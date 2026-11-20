# -*- coding: utf-8 -*-
"""0.56.22: the Pictures menu item's own icon is a camera (the user: "pictures home menu item should have a camera icon,
not a sun/brightness one"). media/aeon/icons/camera.png (96 px, 8 px stroke like the set) was drawn with PIL; this swaps
the item's default in Aeon_H_Icon and its neighbours' variables (every theme reads them). Safe to run again."""
import io
import os

P = os.path.join('1080i', 'Includes_Aeon_Home.xml')
t = io.open(P, encoding='utf-8').read()
n = 0
for k in ('ListItem.Label2', 'Container(9000).ListItem(-3).Label2', 'Container(9000).ListItem(-2).Label2', 'Container(9000).ListItem(-1).Label2',
          'Container(9000).ListItem.Label2', 'Container(9000).ListItem(1).Label2', 'Container(9000).ListItem(2).Label2', 'Container(9000).ListItem(3).Label2'):
    old = '<value condition="String.IsEqual(%s,pictures)">aeon/icons/sun.png</value>' % k
    n += t.count(old)
    t = t.replace(old, old.replace('sun.png', 'camera.png'))
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('swapped', n)
