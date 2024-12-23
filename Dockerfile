FROM public.ecr.aws/lambda/python:3.8

RUN yum -y install file-devel
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && rm requirements.txt
COPY . ${LAMBDA_TASK_ROOT}
CMD ["src.main.lambda_handler"]
