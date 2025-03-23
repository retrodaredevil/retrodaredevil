Firefox
========

I use Firefox.
This page documents some customizations I make to it.

Extensions
------------

* Cookie AutoDelete

  * https://github.com/Cookie-AutoDelete/Cookie-AutoDelete

* Consent-O-Matic

  * https://github.com/cavi-au/Consent-O-Matic

* uBlock Origin

  * https://github.com/gorhill/uBlock

Compact Mode
------------

https://www.askvg.com/tip-restore-compact-mode-density-option-in-firefox-customize-window/

Go to ``about:config`` and enable ``browser.compactmode.show``.
Now right click on the toolbar and click customize toolbar.
Now change the density to compact.

Other about:config settings
-----------------------------

* ``browser.compactmode.show`` mentioned above
* ``extensions.pocket.enabled`` to false
* (Optional) ``services.sync.prefs.sync.extensions.activeThemeID`` to false

  * Context: https://support.mozilla.org/en-US/questions/1330829
  * If you have another computer using Firefox light mode, it will basically force your other devices into that mode too

* ``browser.tabs.groups.enabled`` to true

  * https://techysnoop.com/enable-disable-tab-groups-in-firefox/
