
def compute(n):
  import time, socket
  time.sleep(n)
  host = socket.gethostname()
  return (host, n)

def main():
  import dispy, random
  cluster = dispy.JobCluster(compute)
  import dispy.httpd
  http_server = dispy.httpd.DispyHTTPServer(cluster)
  jobs = []
  for i in range(10):
    job = cluster.submit(random.randint(5, 20))
    job.id = i
    jobs.append(job)
  for job in jobs:
    host, n = job()
    print('%s executed job %s from %s to %s with %s' % (host, job.id, job.start_time, job.end_time, n))
  cluster.print_status()
  http_server.shutdown()

if __name__ == '__main__':
  main()
