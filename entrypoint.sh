sudo docker build -t marvel_impossible .
sudo docker run -it -v $(pwd):/opt/marvel/ marvel_impossible