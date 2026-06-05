# 家纺恢复

触发词：`家纺恢复` `恢复家纺` `fybedding恢复` `恢复fybedding` `家纺项目恢复原状`

## 执行

直接执行 Python 脚本恢复服务器端代码和数据库：

```python
import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('154.201.90.148', username='root', password='vpciVQWB0935', timeout=30, allow_agent=False, look_for_keys=False)

backup = '/www/backup/fybedding_20260523_103421'

steps = [
    (f'rm -rf /www/wwwroot/fybedding', '清除当前代码'),
    (f'tar xzf {backup}/code/fybedding_full.tar.gz -C /www/wwwroot', '恢复代码'),
    (f'zcat {backup}/db/jiafang_mechpart.sql.gz | mysql -u jiafang_mechpart -pc5QCNQZDQ8QrK3mH jiafang_mechpart', '恢复数据库'),
    ('nginx -s reload', '重载nginx'),
]

for cmd, desc in steps:
    stdin, stdout, stderr = c.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    status = '✅' if not err or 'Warning' in err else '❌'
    print(f'{status} {desc}')
    if err and 'Warning' not in err:
        print(f'   ERR: {err[:200]}')

c.close()

# 验证
print('\n验证：')
for p in ['/', '/collections', '/about', '/contact', '/dealer/login']:
    try:
        r = __import__('urllib.request').request.urlopen(f'http://jiafang.mechpart.io{p}', timeout=10)
        print(f'  {p:20s} -> {r.status}')
    except Exception as e:
        print(f'  {p:20s} -> ❌ {e}')
```

恢复后告知爹各页面状态。
