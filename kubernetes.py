pod_name = ''
namespace = ''
container_name = ''
kub_image = ''
mount_path = ''
n_gpu = 1
from pydantic import BaseModel


kub_cfg = {
  'apiVersion': 'v1',
  'kind': 'Pod',
  'metadata': {
    'name': pod_name,
    'namespace': namespace
  },
  'spec': {
    'containers': [{
      'name':
      container_name,
      'image':
      kub_image,
      'resources': {
        'limits': {
          'nvidia.com/gpu': n_gpu
        }
      },
      'command': ["/bin/bash", "-c"],
      'args': ['pip install tqdm; sleep infinity'],
      # 'args': ['conda env update --file env.yml; sleep infinity'],
      'volumeMounts': [
        {
          'mountPath': mount_path,
          'name': mount_path.split('/')[-1]
        },
      ]
    }],
    'volumes': [
      {
        'name': 'scb-usra',
        'persistentVolumeClaim': {
          'claimName': 'scb-usra'
        }
      },
    ],
    'restartPolicy':
    'Never',
  },  # spec
}

class Kubernetes(BaseModel):
  kub_image: str
  mount_path: str
  namespace: str

  n_gpu: int = 1
  pod_name: str = 'pod'
  container_name: str = 'container'
  link_cmd: str = 'ln -s /cephfs ~/cephfs'
  last_pod_created: str = None

  @property
  def get_pods(self):
    return f'kubectl get pods -n {self.namespace}'

  @property
  def get_config(self):
    return 'kubectl config view'

  repo: str = ''


### Trash functions, maybe useful


def remove_indent(str_block: str):
  lines_all = str_block.splitlines()
  lines = [l for l in lines_all if re.match(r'\W*\w+', l)]
  first = lines[0]
  indent = len(first) - len(first.lstrip())
  no_indent_lines = [line[indent:] for line in lines]
  return '\n'.join(no_indent_lines)


def tab2space(str_block: str):
  return str_block.replace('\t', '    ')


def enter_pod(ii, pod_yaml: str = None):
  pod_yaml = pod_yaml or ii.last_pod_created
  """-i, --stdin=false:
    Pass stdin to the container

  -t, --tty=false:
    Stdin is a TTY"""
  run_cmds(f'kubectl exec -f {pod_yaml} -n {ii.namespace} -it -- /bin/bash')


# apiVersion: v1
# kind: Pod
# metadata:
# name: x
# namespace: y
# spec:
# containers:
# - name: scb-env-one
# 	image: image
# 	command: ["/bin/bash", "-c"]
# 	args: [". activate base; sleep infinity"]
# 	volumeMounts:
# 	- mountPath: /path
# 		name: path
# 	resources:
# 	limits:
# 		memory: 10Gi
# 		cpu: "1"
# 	requests:
# 		memory: 10Gi
# 		cpu: "1"
# volumes:
# - name: name
# 	persistentVolumeClaim:
# 	claimName: name

# kubectl create -f - << EOF
# <contents you want to deploy>
# EOF

### Other useful cli

# kubectl get nodes -L nvidia.com/gpu.product

# kubectl exec -it test-pod -- /bin/bash get into the pod
# 	`kubectl create -f cpu_pod.yaml` to create a pod

# `kubectl get pods -n scb-usra` to check the pod status

# `kubectl exec ata-pod -n scb-usra -it bash` to enter the pod

# `kubectl delete pod ata-pod -n scb-usra` to delete a pod
