import { useEffect, useRef, useState } from "react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

async function executeQuery(query) {
    try {
        const response = await callAction({
            name: "execute_sql_query_action",
            payload: { query }
        });
        const result = response.response;
        if (!result) {
            throw new Error('No data received from server');
        }

        if (result.error) {
            throw new Error(result.error);
        }

        return {
            data: result.rows || [],
            statistics: result.statistics || {
                response_time_seconds: 0.0,
                rows_read: 0,
                bytes_read: 0
            }
        };
    } catch (error) {
        console.error('Error executing query:', error);
        throw error;
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}

function Editor() {
    const chartRef = useRef(null);
    const [sqlQuery, setSqlQuery] = useState(props?.sql || '');
    const [vegaSpec, setVegaSpec] = useState(JSON.stringify(props?.spec || {}, null, 2));
    const [isLoading, setIsLoading] = useState(false);
    const [currentData, setCurrentData] = useState(null);
    const [queryStats, setQueryStats] = useState(null);

    const handleRunQuery = async () => {
        setIsLoading(true);
        try {
            const { data, statistics } = await executeQuery(sqlQuery);
            setCurrentData(data);
            setQueryStats(statistics);

            let spec = JSON.parse(vegaSpec);
            const mergedSpec = {
                ...spec,
                data: { values: data }
            };

            await vegaEmbed(chartRef.current, mergedSpec, {
                renderer: 'svg',
                actions: false
            });
        } catch (error) {
            console.error(error);
            alert('Failed to execute query: ' + error.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpdateSpec = () => {
        try {
            let spec = JSON.parse(vegaSpec);
            const mergedSpec = {
                ...spec,
                data: { values: currentData || [] }
            };

            vegaEmbed(chartRef.current, mergedSpec, {
                renderer: 'svg',
                actions: false
            });
        } catch (error) {
            console.error(error);
            alert('Invalid Vega-Lite specification JSON');
        }
    };

    useEffect(() => {
        if (window.vegaEmbed && props?.spec && props?.sql) {
            setSqlQuery(props.sql);
            setVegaSpec(JSON.stringify(props.spec, null, 2));
            handleRunQuery();
        }
    }, [props?.spec, props?.sql]);

    return (
        <div className="editor w-full">
            <div className="visualization-container w-full flex justify-center">
                <div
                    ref={chartRef}
                    className="w-full"
                    style={{
                        width: '100%',
                        position: 'relative'
                    }}
                />
            </div>

            {queryStats && (
                <Card className="mt-8 mb-4">
                    <CardContent className="pt-6">
                        <div className="flex gap-6 text-sm justify-center">
                            <div className="flex items-center gap-2">
                                <span className="text-muted-foreground">Time:</span>
                                <span className="font-medium">{queryStats.response_time_seconds.toFixed(3)}s</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="text-muted-foreground">Scanned Rows:</span>
                                <span className="font-medium">{queryStats.rows_read.toLocaleString()}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="text-muted-foreground">Scanned Bytes:</span>
                                <span className="font-medium">
                                    {formatBytes(queryStats.bytes_read)}
                                </span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}

            <Accordion type="single" collapsible className="mt-8">
                <AccordionItem value="sql-query">
                    <AccordionTrigger>SQL Query Editor</AccordionTrigger>
                    <AccordionContent>
                        <div className="space-y-4">
                            <textarea
                                value={sqlQuery}
                                onChange={(e) => setSqlQuery(e.target.value)}
                                className="w-full h-48 p-4 font-mono text-sm bg-muted rounded-md"
                                placeholder="Enter your SQL query here..."
                            />
                            <Button
                                onClick={handleRunQuery}
                                disabled={isLoading || !sqlQuery.trim()}
                            >
                                {isLoading ? 'Running...' : 'Run Query'}
                            </Button>
                        </div>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="vega-spec">
                    <AccordionTrigger>Vega-Lite Specification</AccordionTrigger>
                    <AccordionContent>
                        <div className="space-y-4">
                            <textarea
                                value={vegaSpec}
                                onChange={(e) => setVegaSpec(e.target.value)}
                                className="w-full h-96 p-4 font-mono text-sm bg-muted rounded-md"
                                placeholder="Enter your Vega-Lite specification here..."
                            />
                            <Button
                                onClick={handleUpdateSpec}
                                disabled={!currentData}
                            >
                                Update Visualization
                            </Button>
                        </div>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </div>
    );
}

export default Editor;