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

  The service which will be contacted by the device if it will be switched on
  after delivery by the customer.
  The service will return the URL address of the IOT Platform Service

- IOT Platform Service

  This service is the network-based manager mentioned in the chapter above
  and is running in the customer environment.
  The IoT platform provides new security credentials to the device.
  The credentials programmed during device initialization are now replaced
  with the new credentials. From now this service will be the contact for the
  device to the IOT Platform of the customer.

For more information:

[https://secure-device-onboard.github.io/docs/latest/#secure-device-onboard-entities](https://secure-device-onboard.github.io/docs/latest/#secure-device-onboard-entities)

## Device Installation and Onboarding Workflow

![Onboarding Workflow](/assets/images/sdo.png)

1. The manufacturer installs the device together with an application which
   can communicate with the three services described above. This application
   uses the [Client SDK](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/)
   for the communication.
   Additional information about serial number, product ID, URL of the
   Manufacturing Toolkit (Service) has also to be set on the device.
2. When the device will be switched on, the device sends serial Nr.,
   Product ID, ... to the Manufacturing Service.
   This returns the credentials and the URL of Rendezvous Service to the device.
3. The device will be shipped to the customer.
4. The manufacture generates an ownership voucher which includes the device
   information. This voucher will be sent to the IoT Platform service provider
   via either a file or through B2B integration. The provider registers the
   ownership voucher with the Rendezvous Service by importing the voucher into the
   IOT Platform Service. This service will transfer the voucher to the Rendezvous Service.
   So the Rendezvous Service is now aware about the shipped device.
5. When the device has arrived the customer his only task will be to connect
   the device to internet.
6. The device contacts the Rendezvous Service and this service will provide the
   connection information to the IOT Platform Service, if the device is known.
   If not, the device will have to try it again after a while. It could be that
   the Rendezvous Service has not already gotten the information.
7. After receiving the IoT Platform URI, the device contacts the IoT platform.
   The regarding IoT platform service provides new security credentials.
   The credentials programmed during device initialization are now replaced
   with the new credentials.
8. After the connection between the device and the IoT Platform has been
   established, the device can communicate with the IoT Platform service.
   Special "Modules" will be used for that. More about it in the example.

The workflow is a little bit simplified to get a faster overview.
But for more information:

[https://secure-device-onboard.github.io/docs/latest/#the-secure-device-onboard-process](https://secure-device-onboard.github.io/docs/latest/#the-secure-device-onboard-process)

   

# Example

We are concentrating us more or less on the setup of the device with
openSUSE-MicroOS together with an application which uses the
[client-sdk](https://github.com/secure-device-onboard/client-sdk) in order to connect
to the different SDO services.

## Setup the environment and start the three needed services

First of all we have to setup all needed services on a local machine. The services are
written in Java and run on Apache Tomcat.

SDO provides a testing environment
[all-in-one-demo](https://github.com/secure-device-onboard/all-in-one-demo) with which
we can run all three needed services.
The best way is to build the environment by using
[Docker](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/build/README.md).
After successful build, the demo package is available at *demo/aio.tar.gz*.
The build can now be run as a Docker Service described
[here](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#run-as-docker-service).

The services can be accessed via the URL "localhost" and the port "8080". Se we have to change the URL
to a real IP address via a
[REST interface](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#configuring-all-in-one-demo) of the All-In-One demo by using
[curl or postman](https://stackoverflow.com/questions/13782198/how-to-do-a-put-request-with-curl):
- Generate a file called *redirect.properties*.
- Send it via a PUT request to the All-In-One Demo
The content of the file and the PUT request is explained
[here](https://github.com/secure-device-onboard/all-in-one-demo/blob/master/container/overlay/README.md#configuring-all-in-one-demo-for-remote-sdo-client)

Now the three services should be access able and we can setup a device in order to see how the
boarding process works....

## Preparing a device for delivery

### Installing a device

The device should run with openSUSE-MicroOS by using an application which will communicate with
the three SDO services. This application is running as an own service (sdoclient.service) and should
be started automatically while starting the device. The service is packaged in a 
[RPM](https://build.opensuse.org/package/show/home:schubi2/sdo-client) and uses the
[Secure Device Onboard Client SDK](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/) in order to communicate with the three SDO services, running under the
All-In-One demo.

One way to install and to configure the device is to use AutoYaST. The regarding AutoYaST configuration
file can be found [here](https://github.com/schubi2/sdo-client/blob/main/autoinst.xml).
AutoYaST installs openSUSE-MicroOS together with the *sdoclient service* and sets the URL for the comminication to
the *Manufacturing Toolkit (Service)* running under the All-In-One demo. The URL has to be adapted to the right
IP address in the post-install script of the AutoYaST configuration file.
Besides that, the installation workflow is asking for the serial and model number of the device:

![AutoYaST-screenshot](/assets/images/register.png)

This information will be sent during the first connect to the Manufacturing Toolkit (Service).

### Initialize the device

After the first boot of the device the *sdoclient service* will be started and he sends all
information e.g. product ID, serial number... to the *Manufacturing Service*.
This returns the credentials and the URL of the *Rendezvous Service* to the device.
This information will be stored on the device.

The process can be followed in the log file */var/log/sdo-client.log*:

```
16:41:44:115 Starting Secure Device Onboard
16:41:44:115 Platform HMAC key size is zero, DI not done!
'/usr/share/sdo-client/data/mfg_proxy.dat' with proxy info absent
'/usr/share/sdo-client/data/rv_proxy.dat' with proxy info absent
'/usr/share/sdo-client/data/owner_proxy.dat' with proxy info absent
16:41:44:116 HMAC computed successfully!
16:41:44:116 Reading Ownership Credential from blob: Normal.blob
16:41:44:116 Device is ready for DI
16:41:44:116 
-----------------------------------------------------------------------------------
                                    Starting DI
-----------------------------------------------------------------------------------
16:41:44:116 Manufacturer Port = 8080.
16:41:44:117 Connecting to manufacturer Server
16:41:44:117 Proxy enabled but Not set
16:41:44:117 using IP
16:41:44:121 Rest Header write returns 156/156 bytes
16:41:44:121 REST:header(156):POST http://154.120.3.19:8080/mp/113/msg/10 HTTP/1.1
...
16:41:51:634 sdo_rendezvous_read started
16:41:51:634 Adding to rvlst
16:41:51:634 Added to rvlst, 1 entries
16:41:51:634 sdo_rendezvous_list_read read
...
16:41:51:634 Connecting to manufacturer Server
16:41:51:634 Proxy enabled but Not set
16:41:51:634 using IP
16:41:51:634 Rest Header write returns 182/182 bytes
...
16:41:53: 28 Writing to Normal.blob blob
16:41:53: 28 HMAC computed successfully!
16:41:53: 28 Writing to Mfg.blob blob
16:41:53: 28 HMAC computed successfully!
16:41:53: 28 Writing to Secure.blob blob
16:41:53: 28 Generating platform IV of length: 12
16:41:53: 28 Generating platform AES Key of length: 16
16:41:53: 28 Device credentials successfully written!!
16:41:53: 28 
------------------------------------ DI Successful --------------------------------------
```

After that, the *sdoclient service* will be stopped.

The device can be switched off and is ready for sending it to the customer.

## Communication between the device and the IOT Platform of the customer

### Connecting the device to the IOT Platform of the customer

The next time when the device has been booted the *sdoclient service* contacts the *Rendezvous Service*
and receives the URL of *IOT Platform Service*.

The process can be followed in the log file */var/log/sdo-client.log*:

```
16:45:15:181 Starting Secure Device Onboard
'/usr/share/sdo-client/data/mfg_proxy.dat' with proxy info absent
'/usr/share/sdo-client/data/rv_proxy.dat' with proxy info absent
'/usr/share/sdo-client/data/owner_proxy.dat' with proxy info absent
16:45:15:182 HMAC computed successfully!
16:45:15:182 Reading Ownership Credential from blob: Normal.blob
16:45:15:182 Byte Array len 20
16:45:15:182 There should be 1 entries in the rvlst
16:45:15:182 rv_index 0
16:45:15:182 New rv allocated 0x5621b0aba970
16:45:15:182 sdo_rendezvous_read started
16:45:15:182 Adding to rvlst
16:45:15:182 Added to rvlst, 1 entries
16:45:15:182 sdo_rendezvous_list_read read
16:45:15:186 Device is ready for Ownership transfer
16:45:15:187 Byte Array len 35
16:45:15:187 HMAC computed successfully!
16:45:15:187 Reading Mfg block
16:45:15:187 
------------------------------------------------------------------------
                           Starting TO1
------------------------------------------------------------------------
16:45:15:187 Connecting to Rendezvous server
16:45:15:187 Proxy enabled but Not set
16:45:15:187 using IP
16:45:15:188 Rest Header write returns 155/155 bytes
16:45:15:188 REST:header(155):POST http://154.120.3.19:8080/mp/113/msg/30 HTTP/1.1
...
16:45:15:194 SDOProtTO1: Received message type 0 : 48 bytes
16:45:15:194 Byte Array len 20
16:45:15:194 Received n4: [264DACEA688E972C7E3E839A3CC9256B]
16:45:15:194 Received ecdsa EB of len: 0
16:45:15:194 Starting SDO_STATE_TO1_SND_PROVE_TO_SDO
16:45:15:194 Complete SDO_STATE_TO1_SND_PROVE_TO_SDO
16:45:15:194 
_starting SDO_STATE_TO1_RCV_SDO_REDIRECT
16:45:15:194 Connecting to Rendezvous server
16:45:15:194 Proxy enabled but Not set
16:45:15:194 using IP
16:45:15:194 Rest Header write returns 354/354 bytes
16:45:15:195 REST:header(354):POST http://154.120.3.19:8080/mp/113/msg/32 HTTP/1.1
...
16:45:15:669 
_starting SDO_STATE_TO1_RCV_SDO_REDIRECT
16:45:15:669 SDOProtTO1: Received message type 0 : 249 bytes
16:45:15:669 Received redirect: [IPv4:154.120.3.19]
16:45:15:669 Complete SDO_STATE_TO1_RCV_SDO_REDIRECT
16:45:15:669 
------------------------ TO1 Successful ---------------------------------
```

With the next call the *sdoclient service* establish the connection to the
*IOT Platform Service* of the customer and receives new security credentials.

*/var/log/sdo-client.log*:

```
-------------------------------------------------------------------------
                            Starting TO2
-------------------------------------------------------------------------
16:45:15:669 kex name (ECDH) used
16:45:15:669 compute_publicB started
16:45:15:669 compute_publicB complete
16:45:15:669 SDO_STATE_T02_SND_HELLO_DEVICE: Starting
16:45:15:669 Sending n5: [1CB64535D72C1F8D538AC6FD582B61FC]
16:45:15:669 SDO_STATE_T02_SND_HELLO_DEVICE: Complete
16:45:15:669 SDO_STATE_TO2_RCV_PROVE_OVHDR: Starting
16:45:15:669 Proxy enabled but Not set
16:45:15:669 using DNS: 154.120.3.19
16:45:15:669 Resolving DNS-URL: <154.120.3.19>
16:45:15:669 Connecting to owner server
16:45:15:670 Proxy enabled but Not set
16:45:15:670 using IP
16:45:15:670 Rest Header write returns 156/156 bytes

16:45:15:670 REST:header(156):POST http://154.120.3.19:8080/mp/113/msg/40 HTTP/1.1
...
Device onboarded successfully.
16:45:16:567 SDO_STATE_TO2_SND_DONE: Starting
16:45:16:567 
***** REUSE feature enabled *****
16:45:16:567 *****Reuse triggered.*****
16:45:16:567 Data protection key rotated successfully!!
16:45:16:567 Writing to Normal.blob blob
16:45:16:568 HMAC computed successfully!
16:45:16:568 Writing to Mfg.blob blob
16:45:16:568 HMAC computed successfully!
16:45:16:568 Writing to Secure.blob blob
16:45:16:568 Updated device with new credentials
16:45:16:568 SDO_STATE_TO2_RCV_DONE_2: Starting
16:45:16:568 Connecting to owner server
16:45:16:568 Proxy enabled but Not set
16:45:16:568 using IP
16:45:16:569 Rest Header write returns 211/211 bytes

16:45:16:569 REST:header(211):POST http://154.120.3.19:8080/mp/113/msg/50 HTTP/1.1
...
------------------------------------ TO2 Successful --------------------------------------

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@Secure Device Onboarding Complete@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

```

From now on the device can communicate via the *sdoclient service* with the
*IoT Platform service* of the customer. Special "Modules" will be used for that.
This will be described in next chapter.

### Communication between customer IoT Platform and the device via modules

The device application (in our case the sdoclient service) can define special task in
different modules.
Firmware update, key provisioning, and Wi-Fi* network setup are some examples of common
functionality that could be provided by modules.
These modules will be statically linked to the device application and will
be driven by callbacks. They will be announced to the *IoT Platform service* which
also has to provide a counterpart module. Both modules can communicate in both directions.

![Modules](/assets/images/3-Service_Info_Exchanges_between_Device_and_Owner_Server.jpeg)

In our example the *sdoclient service* includes the module *sdo_sys* which copies the file
*payload.bin* and *linux64.sh* from the customer IoT Platform into the device directory
*/var/lib/sdo-client/data*. The script *linux64.sh* will be executed on the device when the
copy has been finished.

For more information how to set up a module and which protocols are used for it:
[https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/#device-specific-modules](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/#device-specific-modules)


# References

[https://www.lfedge.org/projects/securedeviceonboard/](https://www.lfedge.org/projects/securedeviceonboard/)
[https://secure-device-onboard.github.io/docs/latest/](https://secure-device-onboard.github.io/docs/latest/)
[https://secure-device-onboard.github.io/docs/latest/reference/](https://secure-device-onboard.github.io/docs/latest/reference/)
[https://github.com/secure-device-onboard](https://github.com/secure-device-onboard)
[https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/](https://secure-device-onboard.github.io/docs/latest/client-sdk/client-sdk-reference-guide/)



