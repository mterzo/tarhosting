# Hosting and extracting tarballs

Tarhosting, is a simple way to take compressed tarballs and host their
content.  This is designed to be a quick and easy solution to present
CI docs and test results inside of CI.

# Docker Quickstart
```
docker run -d -v /srv/docker/tarhosting:/static -p 6080:80 terzom/tarhosting
```

# API

## Get
To retive data publish
```
curl http://<host>:<port>/static/<directory>/path
```

## POST /deploy
Publish a tarball.

To pulish static conten stored in `html.tgz` and deploy it to the directory
abc.

```
curl -X POST -F file=@html.tgz http://localhost:5000/deploy/abc
```

This can also be publish into a sub directory

```
curl -F file=@html.tgz http://localhost:5000/deploy/abc/def/ghi
curl http://localhost:5000/static/abc/def/ghi/index.html
```

## GET /undeploy
To clean up directories use undeploy.  This is a recusrive operation, so it will
start at top level.

```
curl ttp://localhost:5000/undeploy/abc/def/ghi
```

# Gitlab CI intgration
This is the entire purpose to deploy documentation and test results from CI.  This service is provided with
pages inside of gitlab which is a really nice feature. Though if you running CE you don't have that option to host content.

```
stages:
  - Test
  - deploy

unit2.7:
  image: python:2.7
  before_script:
    - pip install -r requirements-dev.txt
    - pip install -r requirements.txt
  stage: Test
  script:
    - py.test --cov=reg
    - coverage html
  after_script:
    - tar -C htmlcov -zcf htmlunit.tar.gz .
  artifacts:
    expire_in: 1 week
    paths:
      - htmlunit.tar.gz
      
coveragereport:
  stage: deploy
  dependencies:
    - unit2.7
  script:
    - curl -v -X POST -F file=@htmlunit.tar.gz  http://<HOST>:<PORT>/deploy/${CI_PROJECT_NAME}/${CI_BUILD_REF_NAME}
  when: manual
  environment:
    name: reviews/$CI_BUILD_REF_NAME
    url: http://<HOST>:<PORT>/static/<PROJECT>/$CI_BUILD_REF_NAME/
    on_stop: retire_coveragereport

retire_coveragereport:
  stage: deploy
  when: manual
  script:
    - curl http://<HOST>:<PORT>/undeploy/${CI_PROJECT_NAME}/${CI_BUILD_REF_NAME}
  environment:
    name: reviews/$CI_BUILD_REF_NAME
    action: stop
```

