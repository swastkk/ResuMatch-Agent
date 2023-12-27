import subprocess

from uagents import Agent, Context, Model


class Message(Model):
    message: str


RECIPIENT_ADDRESS = "agent1qv2l7qzcd2g2rcv2p93tqflrcaq5dk7c2xc7fcnfq3s37zgkhxjmq5mfyvz"  # Replace with the actual address of Agent1

agent2 = Agent(
    name="agent2",
    port=8000,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)


@agent2.on_interval(period=2.0)
async def send_message(ctx: Context):
    # ctx.logger.info("{}", ctx.address)
    await ctx.send(RECIPIENT_ADDRESS, Message(message="Hello there bob."))


@agent2.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    subprocess.run(["notify-send", msg.message])


if __name__ == "__main__":
    agent2.run()
