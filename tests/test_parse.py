from greenbutton.parse import parse_feed


def test_parse_yields_expected_results():
    ups = parse_feed(
        "C:/Users/jdbax/projects/my-greenbutton-python/tests/testdata/PacificPower_GreenButton_03122023.xml"
    )
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
                        % ", ".join([rq.quality.name for rq in ir.readingQualities]),
                        end="",
                    )
                print("")

    pass
