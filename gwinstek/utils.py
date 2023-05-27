def log_telemetry(timestamp, telemetry):
    """
    Log telemetry
    :param timestamp:
    :param telemetry:
    :return:
    """
    import logging
    log_message = f"{timestamp}: {telemetry}"
    logging.info(log_message)
