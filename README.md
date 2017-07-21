# TinyPngPython
A python implement for tinypng

# 使用方式

第一次运行会在脚本所在目录生成一个 tinypng.ini 文件，然后需要自己去 [tinypng developer API](https://tinypng.com/developers) 申请 API key，将其贴到 tinypng.ini 文件中。

运行的时候直接将需要压缩的图片或者图片所在文件夹作为参数传进去就行。支持多个图片或者文件夹。但对于文件夹不支持子目录查找。

每个免费的 API key 是有 500/月 的配额，可以多申请几个，然后用逗号分隔，配置到 ini 文件中。

压缩之后的图片存放在运行目录的 tinify 目录下。压缩文件夹时，在 tinify 目录下会生成跟源目录相同的目录结构。
