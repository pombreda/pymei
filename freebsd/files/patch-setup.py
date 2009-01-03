--- setup.py.orig	2008-12-05 10:44:16.480892650 +0100
+++ setup.py	2008-12-05 10:44:22.287372244 +0100
@@ -30,7 +30,7 @@
                       'mei.gui.widgets'
                      ],
       data_files   = [
-                      ('/etc', ['example_configuration/pymei.config']),
+                      ('etc', ['example_configuration/pymei.config']),
                       ('share/pymei/data', files_in('data')),
                       ('share/pymei/themes', files_in('themes'))
                      ]
