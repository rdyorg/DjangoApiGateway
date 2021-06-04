from django.db import models


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField("创建时间", auto_now_add=True, editable=False, db_index=True)
    update_time = models.DateTimeField("修改时间", auto_now=True, editable=False, db_index=True)

    class Meta:
        abstract = True


class Server(BaseModel):
    name = models.CharField("名称", max_length=100)
    s_type = models.CharField("服务类型", max_length=10, default="HTTP", blank=True)
    instances = models.CharField("实例列表", max_length=400, default="", blank=True)
    LOAD_BALANCE_TYPE = (
        (1, "轮询"),
        (2, "随机"),
    )
    load_balance_type = models.IntegerField("负载均衡", choices=LOAD_BALANCE_TYPE, default=1, blank=True)

    class Meta:
        managed = True
        db_table = 'gateway_server'
        verbose_name = '服务'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Api(BaseModel):
    """
    最底层api，每个api表示一个单独的接口，是一次单独的请求
    """
    server = models.ForeignKey(Server, related_name="api_server", on_delete=models.DO_NOTHING, verbose_name="服务")
    name = models.CharField("名称", max_length=100)
    METHOD = (
        ("GET", "GET"),
        ("POST", "POST"),
    )
    method = models.CharField("方法", max_length=5, choices=METHOD, default="GET", blank=True)
    PROTOCOL = (
        ("HTTP", "HTTP"),
        ("HTTPS", "HTTPS"),
    )
    protocol = models.CharField("协议", max_length=5, choices=PROTOCOL, default="HTTP", blank=True)
    path = models.CharField("api路径", max_length=300, default="/", blank=True, help_text="必须以/开头", db_index=True)
    timeout = models.IntegerField("超时时间(ms)", default=1000, blank=True)
    involve = models.TextField("入参", blank=True, default="")
    existence = models.TextField("出参", blank=True, default="")

    class Meta:
        managed = True
        db_table = 'gateway_api'
        verbose_name = '接口'
        ordering = ["-id"]

    def __str__(self):
        return self.name


rucan = {
    "headers": {},
    "args": {},
    "data": {},
    "script": {}
}

chucan = {
    "headers": {},
    "data": {},
    "script": {}
}


class Step(BaseModel):
    """
    每个步骤下的所有api异步执行，步骤之间同步执行
    """
    name = models.CharField("名称", max_length=100)
    api = models.ManyToManyField(Api, through="StepApi")
    arrangement = models.ForeignKey("Arrangement", on_delete=models.CASCADE, related_name="step_arrangement",
                                    verbose_name="编排", null=True)
    sort = models.IntegerField("顺序", blank=True, default=1)

    class Meta:
        managed = True
        db_table = 'gateway_step'
        verbose_name = '步骤'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class StepApi(models.Model):
    step = models.ForeignKey(Step, related_name="steps", on_delete=models.CASCADE)
    api = models.ForeignKey(Api, related_name="apis", on_delete=models.CASCADE)
    involve = models.TextField("入参", blank=True, default="")
    existence = models.TextField("出参", blank=True, default="")

    class Meta:
        managed = True
        db_table = 'gateway_step_api'
        verbose_name = '步骤接口表'
        ordering = ["-id"]

    def __str__(self):
        return str(self.step.id)


class Arrangement(BaseModel):
    name = models.CharField("名称", max_length=100)
    desc = models.CharField("描述", max_length=400, default="", blank=True)

    class Meta:
        managed = True
        db_table = 'gateway_arrangement'
        verbose_name = '编排'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Gateway(BaseModel):
    name = models.CharField("名称", max_length=100)

    class Meta:
        managed = True
        db_table = 'gateway_gateway'
        verbose_name = '网关'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Router(BaseModel):
    name = models.CharField("名称", max_length=100)
    gateway = models.ForeignKey(Gateway, on_delete=models.DO_NOTHING, related_name="router_gateway", verbose_name="网关")
    METHOD = (
        ("GET", "GET"),
        ("POST", "POST"),
    )
    method = models.CharField("方法", max_length=5, choices=METHOD, default="GET", blank=True)
    path = models.CharField("api路径", max_length=300, default="/", blank=True, db_index=True)
    arrangement = models.ForeignKey(Arrangement, on_delete=models.DO_NOTHING, related_name="router_arrangement",
                                    verbose_name="编排", blank=True, null=True)
    api = models.ForeignKey(Api, on_delete=models.DO_NOTHING, related_name="router_api", verbose_name="接口",
                            blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gateway_router'
        verbose_name = '路由'
        ordering = ["-id"]
        # path必须唯一
        unique_together = (('path', 'gateway'),)

    def __str__(self):
        return self.name
