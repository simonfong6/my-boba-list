docker container run \
    -it \
    --rm \
    --name my-boba-container \
    --user vscode \
    --mount type=bind,source=/home/ubuntu/Projects/my-boba-list,target=/workspace/my-boba-list \
    --workdir /workspace/my-boba-list \
    --publish 3034:3034 \
    e3cd678e04eb /bin/bash && pip3 install -r requirments.txt
