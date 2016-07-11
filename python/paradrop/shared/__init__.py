import output

log = output.Output(
    header=output.BaseOutput(LOG_TYPES[Level.HEADER]),
    testing=output.BaseOutput(LOG_TYPES[Level.VERBOSE]),
    verbose=output.BaseOutput(LOG_TYPES[Level.VERBOSE]),
    info=output.BaseOutput(LOG_TYPES[Level.INFO]),
    usage=output.BaseOutput(LOG_TYPES[Level.USAGE]),
    perf=output.BaseOutput(LOG_TYPES[Level.PERF]),
    warn=output.BaseOutput(LOG_TYPES[Level.WARN]),
    err=output.BaseOutput(LOG_TYPES[Level.ERR]),
    exception=output.ExceptionOutput(LOG_TYPES[Level.ERR]),
    security=output.BaseOutput(LOG_TYPES[Level.SECURITY]),
    fatal=output.BaseOutput(LOG_TYPES[Level.FATAL]),
    twisted=output.TwistedOutput(LOG_TYPES[Level.INFO]),
    twistedErr=output.TwistedException(LOG_TYPES[Level.ERR])
)
