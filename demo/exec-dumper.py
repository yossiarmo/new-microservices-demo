import time

import sys
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


def exec_commands(api_instance,ns,pod_name,file_to_dump):
    name = pod_name
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace=ns)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        print("Pod %s does not exist. " % name)
        exit(1)
        
    # Calling exec and waiting for response
    #exec_command = ['/bin/cat',file_to_dump]
    exec_command = sys.argv[3:]
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  ns,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print("Response: \n" + resp)


import os

def main():
    open('/tmp/token','w').write(os.environ['TOKEN'])
    open('/tmp/cert','w').write(os.environ['CERTIFICATE'])
    config.load_kube_config()
    config.incluster_config.InClusterConfigLoader(
        token_filename='/tmp/token',
        cert_filename='/tmp/cert',
        try_refresh_token=False).load_and_set()
    core_v1 = core_v1_api.CoreV1Api()
    ns = sys.argv[1]
    pod = sys.argv[2]
    file_to_dump = sys.argv[3]
    exec_commands(core_v1,ns,pod,file_to_dump)


if __name__ == '__main__':
    main()

oldtoken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ik02OXd6TlBjSFVtNTQ2T0swSEtVNFByaVZXd3FVU01fWGZyRkxsSmc2RE0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJoaXBzdGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcTk1dngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjZkZmRkNGY4LWJhMWEtNDkyOS1iN2FmLTAyZjRmMGZjZjFmYSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpoaXBzdGVyOmRlZmF1bHQifQ.I2kCjPrOdXHNtsmljQGzrcpOMzCuLQndbmrFugH40HTF6_3G94O_EQKH1gOALQuZJnnvM5KlGb8Am4RCC18T80Icw8jTbBelQ0rJv8aQsDVVfYHy-HXVEW9F4q8OJt7aAZ9QA3m5NjE9iSKvpoNcr2VE7nIK4gQSQ58dTHjZowfcK0QNZ-6C4JjuULwcXFrRPi_R7FGrwmqfCz6tIP0Tqd_DpLrWr-rSF-8MKRaIEZG67G2cCzR7ug81d0_0Vh23tzT90rI8edg2mCL2ZdbzJQjUQTvR4nyG8GN9m6vnq2A30M00RYBZbtefDc1XoHtLBpyhQwh5WzFG8IwcPPADaA'
oldcert = '''-----BEGIN CERTIFICATE-----
MIIDKzCCAhOgAwIBAgIRAKoMUjNftDR6BY0BgJP7ZfowDQYJKoZIhvcNAQELBQAw
LzEtMCsGA1UEAxMkYjY5NDA2MWMtODkzYy00MDVkLWIyNjktYWZkZGViMzg1YmJj
MB4XDTIxMDEyMDE1Mzc0OFoXDTI2MDExOTE2Mzc0OFowLzEtMCsGA1UEAxMkYjY5
NDA2MWMtODkzYy00MDVkLWIyNjktYWZkZGViMzg1YmJjMIIBIjANBgkqhkiG9w0B
AQEFAAOCAQ8AMIIBCgKCAQEAtEY5zq922ocSBWII02Q5scRX2jd/k9OVkghGMJoB
4fxfppksNoXWfxZO22P7U5wBht3i2T4W7kcWVyERlmKCS690RZqf2Tnk/ntxp6WX
21QG4OoXmPzm2/o88Z3flcCQqq1vhUA/D907reR7mXTg8kvboQe6G9bn+Q4sFPOV
KjP7ssnZhMXtAfsr3dCy9PExrhLG5cJc3911HJxoOYwOEH7+m0Js3IelW73LgxYO
GXJmpFcLuuzwHYXRW+D/diHdmuoYW8RqeglHQ39pp0H/aNuFxJhJcQanq+eOoKpR
T/baofxKd/AAhwN41K+gj0/2aCzt5JssRrtU/mWOCEODEwIDAQABo0IwQDAOBgNV
HQ8BAf8EBAMCAgQwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUxs2BdjPsF5HR
6jDWViyodXKtB3AwDQYJKoZIhvcNAQELBQADggEBAAaGvFF39Z38J12eR8d//rsO
pv5dVWe52dmkjKNCx/WXQwx2YeqORxqmHTJsDCJ9s7lccBr8oyDnsh4UrZ+3H4P5
hkYdIg1FEVSNlajhRM71cEDRlEW1I9eCyFQW04W3t51PtCa24I3GATGrRLZl0p5C
pQxFX084pcWg7dSie1GBAEBF6z4fuCvDJGKOJywOZ3tv8jSc48LEpkGCWFT93Tye
KFL6ebnwOYxIy1dQggqvVwyI+VuKH0ni+g9fHyxanuJoxhII96fPRLLfvEJRw1tm
T3H1yA+rcUluu3IMJ8p12YcRAts/P+4rVw68Ov67W0c9FXg49X8pR+RkUaGZWrw=
-----END CERTIFICATE-----
'''

