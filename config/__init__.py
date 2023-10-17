import environ


@environ.config(prefix="APP", frozen=True)
class AppConfig:
    port: int = environ.var(
        default=8001,
        converter=int,
    )


app_config = environ.to_config(AppConfig)
