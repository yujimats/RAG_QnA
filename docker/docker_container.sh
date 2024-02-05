#!/bin/bash
docker run \
    -it \
    --rm \
    --volume $(pwd)/../src/:/home/rag_qna/ \
    --volume $(pwd)/../data:/home/rag_qna/data \
    --workdir /home/rag_qna/ \
    yujimats_rag_qna:latest
