# samplewebsite

This is a sample web site program by python

# Requirement

docker

# Installation

* Windows(docker toolboxを使用した方が良いかもしれません)
* https://hub.docker.com/editions/community/docker-ce-desktop-windows
* Docker Toolbox
* https://docs.docker.com/toolbox/toolbox_install_windows/

* Mac
* https://hub.docker.com/editions/community/docker-ce-desktop-mac

* Linux
* https://docs.docker.com/engine/install/debian/

# Note

* Usageのコマンドを実行する前にDockerHubにアカウントを作成する必要があります。
* 下記のURLからDockerHubのアカウントを作成してください。
* https://hub.docker.com/

* アカウント作成後、下記のコマンドでログインできるかご確認ください。
```bash
docker login
```

# Usage

```bash
mkdir examples && cd examples
git clone https://github.com/Jp29tkDg79/samplewebsite.git
docker-compose build
docker-compose up -d
```

* mysqlのテーブル情報を確認する場合

```bash
docker-compose exec mysql bash
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD

mysql> show databases;
mysql> use test_database;
mysql> show tables;
mysql> select * from persons;
```

* コンテナ内から抜ける場合
```bash
exit
```

# Author

* JpTkDog
* Jp29tkDg79@users.norely.github.com

# License

"samplewebsite" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

"samplewebsite" is Confidential.
