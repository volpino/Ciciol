Ciciòl
======

Ciciòl aims to be a simple but extremely customizable and lightweight
notifier. Was designed to work with Twitter but its plugin-based structure
makes it extendible for any kind of service.


Getting Started
---------------
* Install from PyPi:
  * ``` pip install ciciol ``` or ``` easy_install ciciol ```
* Install from git:
  * ```
    git clone https://volpino@github.com/volpino/Ciciol.git
    ```
  * ```
    python setup.py install
    ```
* Install python-notify for libnotify support

* Write your own configuration file
  * If you want to use twitter just copy the config file in examples/.
    Get access_key and access_secret with:
    ```
    ciciol --setup twitter
    ```
* Launch ciciol
  ```
  ciciol
  ```

  
What are handlers?
------------------
Handlers are plugins for handling sources of information and extract
interesting notifications from them. For example the Twitter handler looks
for new tweets, filters according to what the user specified in the config
file and sends the notification data to one or more backends.


What are backends?
------------------
Backends are plugins for effectively notify the user using various techniques
(desktop notifications, emails, IRC, ...).


Writing a configuration file
----------------------------
First of all have look at the examples in examples/
Basically in the configuration file you've to specify which handlers and
backends you'd like to use plus optional handler specific configuration.


Contribute
----------

Writing a plugin for Ciciòl is very easy! Start having a look at the existing
plugins.
Feel free to fork this repo, open issues and send pull requests


Development Status
------------------
[![Build Status](https://secure.travis-ci.org/volpino/Ciciol.png?branch=develop)](http://travis-ci.org/volpino/Ciciol)
