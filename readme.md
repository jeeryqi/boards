## 创建数据库

* 生成迁移文件
```
python manage.py makemigrations
```

* 验证sql

```
python manage.py sqlmigrate boards 0001
```
    	
* 应用到数据库

```
python manage.py migrate
```

## 两种插入数据方法

- `board = Board(name='Django', description='This is a board about Django.')`

    `board.save()`
    
- `board = Board.objects.create(name='Python', description='General discussion about Python.')`