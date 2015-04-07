This is a template to create a docker file for BasisTech.
First you need to copy the files

* rlp-with-rws-7.11.0-sdk-amd64-glibc25-gcc41.tar.gz
* rlp-license.xml

into this directory. Then you can do

    $ boot2docker start  # only on Mac OS X
    $ docker build -t basistech .
    $ docker run --name basistech_instance -p 9020:9020 -i -t basistech
    $ boot2docker ip    # only on Mac OS X, on Linux you can use 127.0.0.1
    192.168.59.103

Then you can open your browser and should see the rossetta 
demo running at http://192.168.59.103:9020/rlpdemo

To clean up everything do

    $ docker stop basistech_instance
    $ docker rm basistech_instance
    $ docker rmi basistech
    $ boot2docker stop # only on Mac OS X
