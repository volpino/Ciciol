Ciciòl
======

Ciciòl aims to be a simple but extremely customizable and lightweight
notifier. Was designed to work with Twitter but its plugin-based structure
makes it extendible for any kind of service.


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
Writeme


Contribute
----------

Writing a plugin for Ciciol is very easy! Start having a look at the existing
plugins.
Feel free to fork this repo, open issues and send pull requests
