# loveMahjong

起動
```
docker-compose up
```

起動(background)
```
docker-compose up -d
```

停止
```
docker-copose down
```

serverのみ起動
```
dokcer-compose up server
```

clientのみ起動
```
dokcer-compose up client
```

DBをリセットしたい時(docker rmがされている状態で実行)
```
docker volume rm koi-jan_data-volume
```
