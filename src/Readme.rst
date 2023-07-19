Pardus Power Manager
====================

Sub directories
+++++++++++++++

client
^^^^^^
User application that communicate with service and control power profile and settings.

common
^^^^^^
Common functions that used by service and client

service
^^^^^^^
Power management service. It starts at boot and control power profile.

How to communicate with service
+++++++++++++++++++++++++++++++
You must write json data into `/run/ppm` fifo file. For example:

.. code-block:: python

    import os
    import json
    data = {}
    data["pid"] = str(os.getpid())
    data["new-mode"] = "performance"
    with open("/run/ppm","w") as f:
        f.write(json.dumps(data))

**Note:** pid value required.

If you send a data to service, service will automatically update client status.