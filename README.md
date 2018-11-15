<a href="https://codeclimate.com/github/inarli/github-jira-issue-updater/maintainability"><img src="https://api.codeclimate.com/v1/badges/fd1ed433dc911e48178f/maintainability" /></a>

# Nedir? 
Jira ve Github kullanılan projeler için pull requestteki review sonucuna göre ilgili işi jira üzerinde ilerlettiren küçük bir uygulamadır.

# Nereden çıktı?
İş takibini jira üzerinde yapıyoruz ve github üzerindeki branch isimlendirmemizi de jira issue id ileriyle aynı olacak şekilde belirliyoruz.
Bir iş için pull request açıldıysa jira üzerinde o anki konumu code review oluyor. 
İşin release edilebilmesi veya QA testine başlanabilmesi için code review işleminden geçmiş olması gerekli fakat QA engineer jira üzerinde sadece review edilmiş statüsündeki işlere odaklanıyor.
Bu yüzden github üzerindeki pull request'in review işlemi yapıldıktan sonra otomatik olarak ilerletilmesi gerekiyordu. Bu amaçla küçük bir uygulamaya ihtiyaç duyduk.

# Nasıl Çalışır?
Uygulama basitçe github webhookundan gelen bilgilere göre jira issue'sunu hareket ettirir. Bu işlemi yaparken de github webhook'unu kullanır.

# Neler Gerekli?
1 - Bir jira accountu ve o hesap ile alınmış bir api token. https://id.atlassian.com/manage/api-tokens,

2 - Github reponuzda web hook ekleyebilme yetkisi (yoksa)

3 - Uygulamayı herokuda ayağa kaldıracaksanız bir heroku hesabı.

# Nasıl kullanılır?
1. adım : Öncelikle jira work flowunda transition idlerini bilmeniz gerekli.
Size kod reviewdan geçince geçeceği statünün ve review eden kişi değişiklik isteyince geçeceği statünün transition idleri lazım. Bu ikisini öğrenmek için jira apisini kullanabilirsiniz. Gerekli açıklamalar burada mevcut.
https://docs.atlassian.com/software/jira/docs/api/REST/7.6.1/?_ga=2.159860159.344407607.1542286174-1848267653.1477928327#api/2/issue-getTransitions

2. adım : Bu uygulamayı bir yerde ayağa kaldırın. Heroku'yu tavsiye ederim çünkü uygulama herokuda kolayca çalışır hale gelecek şekilde hazırlandı ve ücretsiz bir dyno işinizi görecektir. Yine de başka bir yol tercih ederseniz siz bilirsiniz, o da kolay. Gunicorn ile kolayca servis edebilirsiniz. Zaten Proc dosyasına bakarsanız heroku da öyle çalıştırıyor. 
3. adım : Uygulamanın adresini ve endpointi github hook servisine vereceğiz. Hangi repo için kullanacaksanız o reponun settings'ine gidin ve web hooks sekmesine geçin. Yeni hook ekleyin, aşağıdaki ekran görüntüleri size yardımcı olacaktır diye umuyorum
![image](https://user-images.githubusercontent.com/1387333/48555337-f762a680-e8f1-11e8-84bd-02b40c6c3a5c.png)
Sayfayı aşağı doğru kaydırın
![image](https://user-images.githubusercontent.com/1387333/48555386-1a8d5600-e8f2-11e8-9e90-be53839a16ba.png)
![image](https://user-images.githubusercontent.com/1387333/48555248-aeaaed80-e8f1-11e8-9b13-c808b0fd033c.png)
4. adım : heroku da bir postgresql database oluşturun ve size vereceği bağlantı adresini projedeki .env dosyasına yazın. Tabi öncesinde .env.dist olan ismini .env olarak değiştirmeyi unutmayın.
5. adım : proje içindeki sql/dump.sql dosyasını bu veritabanına import edin.

Artık github reponuza her yeni pull request açıldığında bu adrese bazı bilgiler gönderecek ve uygulama jira hesabınıza api üzerinden erişerek ilgili issue'nun statüsünü güncelleyecektir.

# Dikkat edilmesi gereken noktalar
Branch isimlerinizin jira issue idleriyle aynı olması gerekli. Örneğin JIRA-1234 isimli bir issue id için bir pull request açtıysanız branch ismi de JIRA-1234 olmalı.

# Teşekkür
@suhaboncukcu

# Destek
Eğer kurulum konusunda sorularınız varsa repoda bir issue açarak sorabilirniz.
