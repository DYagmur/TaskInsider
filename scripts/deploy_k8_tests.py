from kubernetes import client, config
from kubernetes.client.rest import ApiException

def load_k8s_config():
    config.load_kube_config()

def create_pod(pod_spec):
    api_instance = client.CoreV1Api()
    try:
        api_instance.create_namespaced_pod(namespace="default", body=pod_spec)
        print(f"Pod {pod_spec['metadata']['name']} created.")
    except ApiException as e:
        if e.status == 409:
            print(f"Pod {pod_spec['metadata']['name']} already exists. Consider deleting it first.")
        else:
            print(f"Failed to create pod: {e}")

def delete_pod(pod_name):
    api_instance = client.CoreV1Api()
    try:
        api_instance.delete_namespaced_pod(name=pod_name, namespace="default", body={"gracePeriodSeconds": 30})
        print(f"Pod {pod_name} deleted.")
    except ApiException as e:
        print(f"Failed to delete pod: {e}")

def delete_all_chrome_nodes(node_count):
    for i in range(node_count):
        delete_pod(f"chrome-node-{i}")

def check_pod_ready(pod_name):
    api_instance = client.CoreV1Api()
    try:
        pod = api_instance.read_namespaced_pod(name=pod_name, namespace="default")
        return pod.status.phase == "Running" and pod.status.container_statuses[0].ready
    except ApiException as e:
        print(f"Failed to check pod readiness: {e}")
        return False

def execute_tests_on_pod(pod_name):
    command = ["bash", "-c", "python -m unittest discover -s tests -p '*.py'"]
    api_instance = client.CoreV1Api()
    try:
        resp = api_instance.connect_get_namespaced_pod_exec(
            pod_name,
            namespace="default",
            command=command,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
            _preload_content=False)

        while resp.is_open():
            resp.update()
            if resp.peek_stdout():
                print(resp.read_stdout())
            if resp.peek_stderr():
                print(resp.read_stderr())
    except ApiException as e:
        print(f"Failed to execute tests: {e}")

def deploy_resources(node_count):
    controller_pod_spec = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test-controller"},
        "spec": {
            "containers": [
                {
                    "name": "test-controller",
                    "image": "yagmurefe/test-insider:latest",
                    "command": ["python", "controller.py"],
                    "ports": [{"containerPort": 8080}]
                }
            ]
        }
    }

    delete_pod("test-controller")
    create_pod(controller_pod_spec)
    delete_all_chrome_nodes(node_count)

    for i in range(node_count):
        chrome_node_pod_spec = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": f"chrome-node-{i}"},
            "spec": {
                "containers": [
                    {
                        "name": "chrome-node",
                        "image": "selenium/node-chrome",
                        "ports": [{"containerPort": 4444}]
                    }
                ]
            }
        }
        create_pod(chrome_node_pod_spec)

def main(node_count):
    load_k8s_config()
    deploy_resources(node_count)

    for i in range(node_count):
        pod_name = f"chrome-node-{i}"
        if check_pod_ready(pod_name):
            execute_tests_on_pod(pod_name)

if __name__ == "__main__":
    node_count = 1
    main(node_count)
