from nonebot import on_notice, require, get_driver, get_bot
from nonebot.adapters.github import PushEvent, PingEvent, WorkflowRunRequested, WorkflowRunCompleted
from nonebot.adapters.onebot.v11 import Bot

matcher = on_notice()
driver = get_driver()
config = driver.config
superuser = list(config.superusers)[0]


@matcher.handle()
async def _(event: PushEvent):
    require("sevenfield_bot.plugins.global_config")
    from sevenfield_bot.plugins.global_config import global_config
    last_commit_sha = event.payload.head_commit.id[:8]
    commit_counts = len(event.payload.commits)
    main_group = int(global_config.qq_main_group)
    self_id = global_config.qq_self_id
    bot: Bot = get_bot(self_id)
    commits = {
        c.id[:8]: c.message
        for c in event.payload.commits
    }
    commit_str = "\n".join("  {sha}: {message}".format(
        sha=sha, message=message) for sha, message in commits.items())
    message = (f"[CQ:at,qq={superuser}]\n"
               "[GitHub]\n"
               f"您的项目zeithrold/sevenfield-bot已经提交{last_commit_sha}等共{commit_counts}个Git Commit。\n"
               "具体Commit列表如下:\n"
               f"{commit_str}")
    await bot.send_group_msg(group_id=main_group, message=message)


@matcher.handle()
async def _(event: PingEvent):
    require("sevenfield_bot.plugins.global_config")
    from sevenfield_bot.plugins.global_config import global_config
    main_group = int(global_config.qq_main_group)
    self_id = global_config.qq_self_id
    bot: Bot = get_bot(self_id)
    await bot.send_group_msg(group_id=main_group, message=f"[CQ:at,qq={superuser}] [GitHub]刚才GitHub给您发送了一个Ping。")


@matcher.handle()
async def _(event: WorkflowRunRequested):
    require("sevenfield_bot.plugins.global_config")
    from sevenfield_bot.plugins.global_config import global_config
    main_group = int(global_config.qq_main_group)
    self_id = global_config.qq_self_id
    event.payload.workflow_run.name
    bot: Bot = get_bot(self_id)
    message = (
        f"[CQ:at,qq={superuser}]\n"
        "[GitHub]\n"
        "您的项目zeithrold/sevenfield-bot已触发Workflow Run: \n"
        f"{event.payload.workflow_run.path} #{event.payload.workflow_run.run_number}\n"
        "详情请点击链接：\n"
        f"{event.payload.workflow_run.html_url}"
    )
    await bot.send_group_msg(group_id=main_group, message=message)


@matcher.handle()
async def _(event: WorkflowRunCompleted):
    require("sevenfield_bot.plugins.global_config")
    from sevenfield_bot.plugins.global_config import global_config
    main_group = int(global_config.qq_main_group)
    self_id = global_config.qq_self_id
    event.payload.workflow_run.name
    bot: Bot = get_bot(self_id)
    message = (
        f"[CQ:at,qq={superuser}]\n"
        "[GitHub]\n"
        "您的项目zeithrold/sevenfield-bot已完成Workflow Run: \n"
        f"{event.payload.workflow_run.path} #{event.payload.workflow_run.run_number}\n"
        f'运行结果：{"成功" if event.payload.workflow_run.conclusion == "success" else "异常"}'
        "\n"
        "详情请点击链接：\n"
        f"{event.payload.workflow_run.html_url}")
    await bot.send_group_msg(group_id=main_group, message=message)
