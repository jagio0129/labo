# CGIの設定
コロプレスマップを表示するhtmlファイルはかなりの数生成されるので、htmlからリンクで飛べるようにしておきたい。

そこでcgiを利用する。

```
sudo vim /etc/apache2/sites-enabled/000-default.conf
  -  #Include conf-available/serve-cgi-bin.conf
  +  Include conf-available/serve-cgi-bin.conf

sudo vim /etc/apache2/conf-available/serve-cgi-bin.conf
  <Directory "/usr/lib/cgi-bin">
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Require all granted
  + AddHandler text/html .html
  </Directory>

sudo service apache2 restart

sudo mkdir /usr/lib/cgi-bin/html
sudo cp  doc/index.rb /usr/lib/cgi-lib/