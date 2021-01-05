ARG IMAGE_NAME=""
FROM ${IMAGE_NAME}
RUN cd /usr/local/ev_sdk \
        && rm -rf /usr/local/vas/vas_data \
        && wget -O /vas_v4.3_cv3.4.tar.gz https://vas-1256261446.cos.ap-guangzhou.myqcloud.com/vas_v4.3_cv3.4.tar.gz  \
        && tar xf /vas_v4.3_cv3.4.tar.gz  -C / \
        && rm -f /vas_v4.3_cv3.4.tar.gz  \
        && chmod +x /usr/local/vas/vas_start_container.sh 


CMD ["/usr/local/vas/vas_start_container.sh"]
