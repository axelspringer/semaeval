#
# Docker file for BasisTech
#

FROM dockerfile/java:oracle-java7

ENV BT_ROOT /BasisTech/BT_RLP_7.11.0

RUN mkdir -pv ${BT_ROOT}

ADD rlp-with-rws-7.11.0-sdk-amd64-glibc25-gcc41.tar.gz ${BT_ROOT}
COPY rlp-license.xml ${BT_ROOT}/rlp/rlp/licenses/

EXPOSE 9020
# make the container stay running by tailing the log file
# see http://stackoverflow.com/questions/26497580/docker-container-exited-immediately-after-python-script-execution
CMD ${BT_ROOT}/rws/bin/launch.sh start && tail -F ${BT_ROOT}/rws/logs/rws.log
