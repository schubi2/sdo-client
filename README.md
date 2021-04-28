# Secure Device Onboard (SDO)

Secure Device Onboard is an automated “Zero-Touch” onboarding service.
“Onboard” means the process by which a device establishes its first trusted connection with a device management service of the customer.

To more securely and automatically onboard and provision a device on edge hardware, it only needs to be drop shipped to the point of installation, connected to the network and powered up. This zero-touch model simplifies the installer’s role, reduces costs and eliminates poor security practices, such as shipping default passwords.

Device provisioning is the process of installing secrets and network addresses into a device so that the device and its network-based manager are able to connect using a trusted connection.  For example, they may share a secret or have trusted PKI credentials.

When provisioning process (described in next chapter) is finished the device is equipped with the Internet address and public key of its manager in order to communicate with him in the future.

For more general information:
[https://www.lfedge.org/projects/securedeviceonboard/](https://www.lfedge.org/projects/securedeviceonboard/)
[https://secure-device-onboard.github.io/docs/latest/](https://secure-device-onboard.github.io/docs/latest/)


# Onboarding Process

## Processes

While the provisioning process there are mainly three SDO services involved:

- Manufacturing Toolkit (Service)
  The Manufacturing Service initializes the device with credentials and the
  information how the device can connect to the Rendezvous Service when the
  device has been shipped to the customer and will be switched on.
  
- Rendezvous Service
  The service which will be contacted by the device if it will be switched on.
  The service will return the URL address of the IOT Platform Service.

- IOT Platform Service
  This service is the network-based manager mentioned in the chapter above.
  The IoT platform provides new security credentials to the device.
  The credentials programmed during device initialization are now replaced
  with the new credentials. From now this service will be the contact for the
  device to the IOT Platform of the customer.

For more information:
[https://secure-device-onboard.github.io/docs/latest/#secure-device-onboard-entities](https://secure-device-onboard.github.io/docs/latest/#secure-device-onboard-entities)

## Device Installation and Onboarding Workflow

1. The manufacturer installs the device together with an application which
   can communicate with the three services described above. This application
   uses the [Client SDK](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/)
   for the communication.
   Additional information about serial Nr., Product ID, URL of the
   Manufacturing Toolkit (Service) has also to be set on the device.
2. When the device will be switched on the device sends serial Nr.,
   Product Id., ... to the Manufacturing Service.
   This returns the credentials and the URL of Rendezvous Service to the device.
3. The device will be shipped to the customer.
4. The manufacture generates an ownership voucher which includes the device
   information. This voucher will be send to the IoT Platform service provider
   via either a file or through B2B integration. The provider registers the
   ownership voucher with the Rendezvous Service by importing the voucher into the
   IOT Platform Service. This service will transfer the voucher to the Rendezvous Service.
   So the Rendezvous Service is aware now about the shipped device.
5. When the device has arrived the customer his only task will be to connect
   the device to internet.
6. The device contacts the Rendezvous Service and this service will provide the
   connection information to the IOT Platform Service, if the device is known.
   If not the device will have to try it again after a while. It could be that
   the Rendezvous Service has not already gotten the information.
7. After receiving the IoT Platform URI, the device contacts the IoT platform.
   The IoT platform service provides new security credentials. The credentials
   programmed during device initialization are now replaced with the new
   credentials.
8. After the connection between the device and the IoT Platform has been
   established, the device can communicate with the IoT Platform service.
   Special "Modules" will be used for that. More about it in the example.

The workflow is a little bit simplified to get a faster overview.
for more information:
[https://secure-device-onboard.github.io/docs/latest/#the-secure-device-onboard-process](https://secure-device-onboard.github.io/docs/latest/#the-secure-device-onboard-process)

   

# Example

We are concentrating us more or less on the setup of the device with
openSUSE-MicroOS together with an application which uses the
[client-sdk](https://github.com/secure-device-onboard/client-sdk) in order to connect
to the the different SDO services.

## Setup the environment and start the three neede services

First of all we have to setup all needed services on a local machine. The services are
written in Java and run on Apache Tomcat.

SDO provides a testing environment
[all-in-one-demo](https://github.com/secure-device-onboard/all-in-one-demo) with which
we can run all three needed services.
The best way is to build the environment by using
[Docker](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/build/README.md).
After successful build, the demo package is available at demo/aio.tar.gz.
The build can now be run as a Docker Service described
[here](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#run-as-docker-service)

The services can be accessed via the URL "localhost" and the port "8080". Se we have to change the URL
to a real IP address via a
[REST interface](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#configuring-all-in-one-demo) of the All-In-One demo by using
[curl or postman](https://stackoverflow.com/questions/13782198/how-to-do-a-put-request-with-curl):
- Generate a file called redirect.properties
- Send it via a PUT request to the All-In-One Demo
The content of the file and the PUT request is explained
[here](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#configuring-all-in-one-demo-for-remote-sdo-client)

Now the three services should be accessable and we can setup a divice in order to see how the
enboarding process works....

## Installing a device

The device should run with openSUSE-MicroOS by using an application which will communicate with
the three SDO services. This application is running as an own service (sdoclient.service) and should
be started automatically while starting the device. The service is packaged in a 
[RPM](https://build.opensuse.org/package/show/home:schubi2/sdo-client) and uses the
[Secure Device Onboard Client SDK](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/) in order to communicate with the three SDO services running under the
All-In-One demo.

One way to install and to configure the device is to use AutoYaST. The regarding AutoYaST configuration
file can be found [here](https://github.com/schubi2/sdo-client/blob/main/autoinst.xml).
AutoYaST installs openSUSE-MicroOS and the sdoclient service and sets the URL for the comminication to
the three SDO services running under the All-In-One demo. The URL has to be adapted to the right
IP address.
Besides that the installation workflow is asking for the serial and model number of the device:

![Tux, the Linux mascot](/assets/images/register.png)

This information will be sent while the first connect to the Manufacturing Toolkit (Service).

