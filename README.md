SunSetter Retractable Awning
============================


This is a web frontend to the inventory commandline utility inside shade.

It uses the [shade](http://git.openstack.org/cgit/openstack-infra/shade) openstack client library and the [flask](http://flask.pocoo.org/docs/0.10/quickstart/) web microframework.


Usage
=====

Sunsetter requires a ``clouds.yaml`` file to exist in either ``~/.config/openstack/clouds.yaml`` or ``/etc/openstack/clouds.yaml``. This is setup and documented in [os-client-config](http://docs.openstack.org/developer/os-client-config/). For developers you can use a ``clouds.yaml`` file in the current working directory.

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python sunsetter.py
```

Open your browser to ``localhost:5000``

