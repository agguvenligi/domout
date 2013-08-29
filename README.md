DomOut
======

Bu yapıda en önemli adım ise alan adlarının kayıt sürelerinin dolması ile başlayan süreç olmaktadır. Her ne kadar bellek boyut/fiyat oranları artsada insan belleği aksine zamanla dolmakta ve yeni bilgilerin kalıcılığı azalmaktadır. Bu perspektiften bakıldığında yaşanabilecek en büyük sorunlardan bir tanesi sahip olunan alan adının geçerlilik süresinin dolması ve bunula başlayan süreçte alan adının yenilenmeyerek sahipliğinin kaybedilmesi olabilmektedir. 
Mevcut alan adına ait geçerlilik süresi linux sistemlerde bulunan whois komutu ile görülebilmektedir.

Bütün bu işlemleri otomatik olarak kontrol eden ve belirlenen sürenin kalmasından itibaren mail yolu ile bilgilendirme yapan yazılımın kullanımına dair ayrıntılar aşağıda görüldüğü gibi olmaktadır. Öncelikle yazılım temin edilmelidir, yapılandırma dosyası ihtiyaca göre belirlenerek oluşturulmalı ve son olarak çalıştırma hakları verilerek belirli zamanlarda çalıştırılmalıdır.

    # wget https://raw.github.com/agguvenligi/domout/master/DomOut.py

Gerekli yazılımların temin edilerek kurulmasının ardından DomOut yapılandırması belirlenerek çalıştırılması sağlanabilmektedir.

    # wget http://effbot.org/media/downloads/elementtree-1.2-20040618.tar.gz

    # tar -zxvf elementtree-1.2-20040618.tar.gz

    # cd elementtree-1.2-20040618

    # python setup.py install

Ardından DomOut paketi için yapılandırma dosyası ihtiyaca göre oluşturulmalıdır.Yazılım ile birlikte örnek bir yapılandırma dosyası gelmektedir. Dosya içeriği aşağıdaki gibi olmaktadır.

    # cat DomOut.conf

<?xml version="1.0"?>

<domout>

    <email>

        <server>localhost</server>

        <default_mail_to>info@agguvenligi.net</default_mail_to>

        <sender>DomOut@agguvenligi.net</sender>

    </email>

    <domain>

        <name>agguvenligi.net</name>   

        <expire_day>250</expire_day>

    </domain>

</domout>


    #./DomOut.py -f DomOut.conf

    agguvenligi.net -> 250 -> 243
