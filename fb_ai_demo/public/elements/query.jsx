import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

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

        if (!result.success) {
            const fixed_response = await callAction({
                name: "fix_sql_query_action",
                payload: { query }
            });
            const fixed_result = fixed_response.response;
            if (!fixed_result) {
                throw new Error('No data received from server');
            }
            if (fixed_result.fixed) {
                throw new Error('Original query failed to execute with the error: ' + fixed_result.original_error + '. Fixed query: ' + fixed_result.query);
            } else {
                throw new Error('Original query failed to execute with the error: ' + fixed_result.original_error + '. Failed to fix the query: ' + fixed_result.error);
            }
        }

        return {
            rows: result.rows || [],
            column_names: result.column_names || [],
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

function QueryUI() {
    const [sqlQuery, setSqlQuery] = useState(props?.sql || '');
    const [isLoading, setIsLoading] = useState(false);
    const [queryStats, setQueryStats] = useState(null);
    const [queryResult, setQueryResult] = useState(null);
    const [column_names, setColumnNames] = useState([]);
    const [isTableCollapsed, setIsTableCollapsed] = useState(false);

    const handleRunQuery = async () => {
        setIsLoading(true);
        try {
            const { rows, column_names, statistics } = await executeQuery(sqlQuery);
            setQueryResult(rows);
            setColumnNames(column_names);
            setQueryStats(statistics);
        } catch (error) {
            console.error(error);
            alert('Failed to execute query: ' + error.message);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (props?.sql) {
            setSqlQuery(props.sql);
            handleRunQuery();
        }
    }, [props?.sql]);

    return (
        <div className="query-ui w-full space-y-4">
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

            {queryStats && (
                <Card className="mt-4">
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

            {queryResult && (
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm text-muted-foreground">
                            Query Results ({queryResult.length} rows)
                        </span>
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setIsTableCollapsed(!isTableCollapsed)}
                        >
                            {isTableCollapsed ? 'Show Results' : 'Hide Results'}
                        </Button>
                    </div>

                    {!isTableCollapsed && (
                        <div className="rounded-md border">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        {column_names.map((column) => (
                                            <TableHead key={column}>{column}</TableHead>
                                        ))}
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {queryResult.map((row, i) => (
                                        <TableRow key={i}>
                                            {column_names.map((column) => (
                                                <TableCell key={column}>
                                                    {row[column]?.toString() || ''}
                                                </TableCell>
                                            ))}
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default QueryUI; 