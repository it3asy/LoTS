
# iis短文件名枚举漏洞修复
---
 
// 2017/02/12


## 0×1 关于漏洞

[1] [http://soroush.secproject.com/downloadable/microsoft_iis_tilde_character_vulnerability_feature.pdf](http://soroush.secproject.com/downloadable/microsoft_iis_tilde_character_vulnerability_feature.pdf)  
[2] [http://www.acunetix.com/blog/articles/windows-short-8-3-filenames-web-security-problem/](http://www.acunetix.com/blog/articles/windows-short-8-3-filenames-web-security-problem/)  



## 0×2 修复参考

现实环境中，该漏洞主要存在为Windows Server 2003服务器上，本文讨论的修复方案基于Windows Server 2003 + IIS6环境而论。以下是几个公开的解决方案：  

**方案一** 360网站安全给出的修复方案，见[http://webscan.360.cn/vul/view/vulid/1020](http://webscan.360.cn/vul/view/vulid/1020 "IIS短文件名泄露漏洞")，以下引用原文：
>  
>**解决方案：**
> 三种修复方案只有第二和第三种能彻底修复该问题,可以联系空间提供商协助修改.
>
> 方案1.修改注册列表HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\NtfsDisable8dot3NameCreation的值为1,或者，可以直接点此下载，然后运行,再重启下机器。(此修改只能禁止NTFS8.3格式文件名创建,已经存在的文件的短文件名无法移除)。该修改不能完全修复,只是禁止创建推荐使用后面的修复建议  
>
> 方案2.如果你的web环境不需要asp.net的支持你可以进入Internet 信息服务(IIS)管理器 --- Web 服务扩展 - ASP.NET 选择禁止此功能。（推荐）  
>
>方案3.升级net framework 至4.0以上版本.（推荐）  

这个修复方案中：  
1) 方法1只禁止以后创建的文件再生成短文件名，但已经存在的短文件并不会删除，相当于漏洞基本上没修复；  
2) 方法2是特殊情况，不论；  
3) 方法3适合2003以上系统，经实测升级.net到4.0并不会修复漏洞，而4.0之后版本为4.5，已经不支持2003系统。

**方案二** 另一个修复方案，见[http://www.cnblogs.com/lyuec/p/4255095.html](http://www.cnblogs.com/lyuec/p/4255095.html "IIS短文件漏洞修复")，以下引用原文：  
>
> 结合资料整理修复方案：
>
> 1、修改注册表项：（重启服务器生效）  
> HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\NtfsDisable8dot3NameCreation  
> 值为1。
>
> 2、执行DOS命令， fsutil behavior set disable8dot3 1
>
> 3、删除现有的IIS目录重新部署，完成此步骤才能完全修复。

这是一个合理的修复方案，通过步骤1、2禁止以后创建的文件再生成短文件名（这里步骤2是多余的，注[1]）;再通过步骤3删除已经生成的短文件名，从而形成一个禁绝短文件名的严谨逻辑。  
但这个解决方案说的不够具体，步骤3所说的重新部署是个复杂操作但没说实施细节，比如像[http://www.lijiejie.com/iis-win8-3-shortname-brute/](http://www.lijiejie.com/iis-win8-3-shortname-brute/ "IIS短文件名暴力猜解漏洞分析 | 李劼杰的博客")这篇博文中，以下引用原文：
>**4. 漏洞的修复**
>
> 1) 升级.net framework
>
> 2) 修改注册表键值：  
> HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem  
> 修改NtfsDisable8dot3NameCreation为1。  
>
> 3) 将web文件夹的内容拷贝到另一个位置，比如D:\www到D:\www.back，然后删除原文件夹D:\www，再重命名D:\www.back到D:\www  
> 如果不重新复制，已经存在的短文件名则是不会消失的。

上述文中的第3步的实施是有缺陷的，该操作只修复网站根目录，下级目录并没有修复。


***注:**  
[1] 执行命令fsutil behavior set disable8dot3 1和修改注册表HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\NtfsDisable8dot3NameCreation值为1这两个操作功能是一样的.*

## 0x3 修复方案

综上，我们给出如下修复方案：  

第一步: 执行cmd命令(或修改注册表)禁止系统以后再创建短文件名；  
> 执行cmd命令 “```fsutil behavior set disable8dot3 1```”，随后重启系统。  

第二步: 重新部署网站文件以删除已经存在的短文件名。

> 遍历网站目录及其下级目录，通过“**重命名->恢复原名**”操作删除已经创建过的短文件名。 
该操作不适合手动执行，附VBS脚本：

	fix-iis-enum.vbs

	


**0×4 引用&参考**

1) 关于漏洞  
[1] http://soroush.secproject.com/downloadable/microsoft_iis_tilde_character_vulnerability_feature.pdf  
[2] http://www.acunetix.com/blog/articles/windows-short-8-3-filenames-web-security-problem/  
[3] http://www.freebuf.com/articles/4908.html  

2) 关于修复  
[1] http://webscan.360.cn/vul/view/vulid/1020  
[2] http://www.cnblogs.com/lyuec/p/4255095.html  
[3] http://www.lijiejie.com/iis-win8-3-shortname-brute/  
