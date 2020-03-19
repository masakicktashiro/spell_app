FROM mysql:5.7

RUN apt-get update
RUN apt-get install -y vim
#ポートを開ける
EXPOSE 3306

#MySQL設定ファイルをイメージ内にコピー
ADD ./conf.d/my.cnf /etc/mysql/conf.d/my.cnf
#文字コードの設定のセット
ADD ./initdb.d/init.sql /docker-entrypoint-initdb.d/init.sql
#初期化用のSQLファイルのセット
#docker runに実行される
#CMD ["mysqld"]
