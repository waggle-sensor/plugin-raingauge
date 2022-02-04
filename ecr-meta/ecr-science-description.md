# Hydreon RG-15 Data Collector

This plugin works with the [Hydreon RG-15](https://rainsensors.com/products/rg-15/) rain gauge and will periodically sample and publish the following values:

* `env.raingauge.total_acc`. Total accumulation detected since rain gauge powered up.
* `env.raingauge.event_acc`. Total accumulation detected during rain event. This counter is reset 1 hour after the raingauge has detected the last drop of the event.
* `env.raingauge.rint`. Approximate rain intensity. This is calculated over the past minute and extrapolated to the hour.
