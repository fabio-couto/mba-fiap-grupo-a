FROM hadoop-base:0.1.0

VOLUME [ "/hadoop/yarn/timeline" ]
EXPOSE 8188

RUN mkdir -p /hadoop/yarn/timeline

COPY start.sh /
CMD [ "/start.sh" ]