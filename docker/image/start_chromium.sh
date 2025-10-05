#!/usr/bin/env bash
echo "Deleting old chromium locks..."
rm -rf /mnt/data/cache/Single*
echo "Finished deleting old chromium locks."


if [ ! -d "/mnt/data/cache" ]; then
    echo "ERROR: cache mount missing at /mnt/data/cache"
    echo "Please create and mount a volume at /mnt/data/cache"
    echo "Exiting!"
    exit 1
fi
#  --headless=new \

if [ "$LOGGING_ENABLE" = "TRUE" ]; then
  LOGFILE="/mnt/data/logs/chromium.log"
  exec >/dev/null 2>>"$LOGFILE"
   /usr/bin/chromium \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=/mnt/data/cache \
  about:blank &

else
    echo "INFO: Log to file deactivated"
    echo "ERROR: Log mount missing at /mnt/data/logs or set LOGGING_ENABLE to FALSE"
    echo "Continue without logging to file!"
   
    /usr/bin/chromium \
    --headless=new \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu \
    --remote-debugging-port=9222 \
    --user-data-dir="$KLEINBOTCACHE" \
    about:blank &

fi

#start chromium in headless mode with remote debugging enabled
#user has to define the user-data-dir to a writable location and if desired the profile folder can be copied there
/usr/bin/chromium \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir="$KLEINBOTCACHE" \
  about:blank &

# PID speichern (optional)
echo "Chromium started."
