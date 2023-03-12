#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET
from typing import List

from greenbutton import resources
from greenbutton import utils


def parse_feed(filename: str) -> List[resources.UsagePoint]:
    tree = ET.parse(filename)

    usagePoints = []
    for entry in tree.getroot().findall(
        "atom:entry/atom:content/espi:UsagePoint/../..", utils.ns
    ):
        up = resources.UsagePoint(entry)
        usagePoints.append(up)

    meterReadings = []
    for entry in tree.getroot().findall(
        "atom:entry/atom:content/espi:MeterReading/../..", utils.ns
    ):
        mr = resources.MeterReading(entry, usagePoints=usagePoints)
        meterReadings.append(mr)

    for entry in tree.getroot().findall(
        "atom:entry/atom:content/espi:LocalTimeParameters/../..", utils.ns
    ):
        ltp = resources.LocalTimeParameters(entry, usagePoints=usagePoints)

    readingTypes = []
    for entry in tree.getroot().findall(
        "atom:entry/atom:content/espi:ReadingType/../..", utils.ns
    ):
        rt = resources.ReadingType(entry, meterReadings=meterReadings)
        readingTypes.append(rt)

    intervalBlocks = []
    for entry in tree.getroot().findall(
        "atom:entry/atom:content/espi:IntervalBlock/../..", utils.ns
    ):
        ib = resources.IntervalBlock(entry, meterReadings=meterReadings)
        intervalBlocks.append(ib)

    return usagePoints


if __name__ == "__main__":
    ups = parse_feed(sys.argv[1])
    for up in ups:
        print("UsagePoint (%s) %s %s:" % (up.title, up.serviceCategory.name, up.status))
        for mr in up.meterReadings:
            print("  Meter Reading (%s) %s:" % (mr.title, mr.readingType.uom.name))
            for ir in mr.intervalReadings:
                print(
                    "    %s, %s: %s %s"
                    % (
                        ir.timePeriod.start,
                        ir.timePeriod.duration,
                        ir.value,
                        ir.value_symbol,
                    ),
                    end="",
                )
                if ir.cost is not None:
                    print(" (%s%s)" % (ir.cost_symbol, ir.cost), end="")
                if len(ir.readingQualities) > 0:
                    print(
                        "[%s]"
                        % ", ".join([rq.quality.name for rq in ir.readingQualities])
                    )
                else:
                    print("")
