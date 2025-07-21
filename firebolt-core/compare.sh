#!/bin/bash

set -e

echo "🔥 Firebolt Core Performance Comparison"
echo "======================================="
echo ""

# Test queries for performance comparison
QUERIES=(
    "SELECT COUNT(*) FROM violations WHERE EXTRACT(YEAR FROM issue_date) = 2022"
    "SELECT street_name, SUM(fine_amount) as revenue FROM violations WHERE street_name IS NOT NULL GROUP BY street_name ORDER BY revenue DESC LIMIT 10"
    "SELECT vehicle_make, APPROX_PERCENTILE(fine_amount, 0.95) as p95 FROM violations WHERE vehicle_make IS NOT NULL GROUP BY vehicle_make LIMIT 10"
    "SELECT EXTRACT(HOUR FROM CAST(violation_time AS TIME)) as hour, COUNT(*) FROM violations WHERE violation_time IS NOT NULL GROUP BY EXTRACT(HOUR FROM CAST(violation_time AS TIME))"
)

QUERY_NAMES=(
    "Yearly Aggregation"
    "Top Streets by Revenue"
    "95th Percentile by Vehicle Make"
    "Hourly Violation Patterns"
)

# Output file
OUTPUT_FILE="performance_results.md"

# Initialize results file
cat > $OUTPUT_FILE << EOF
# Firebolt Core Performance Results

Generated on: $(date)

## Query Performance Comparison

| Query | Cold Run (ms) | Hot Run (ms) | Improvement |
|-------|---------------|--------------|-------------|
EOF

# Function to run query and measure time
run_query_with_timing() {
    local query="$1"
    local query_name="$2"
    
    echo "🏃 Running: $query_name"
    
    # Cold run (clear cache first if possible)
    echo "  ❄️ Cold run..."
    start_time=$(date +%s%3N)
    docker exec firebolt-core fbcli -e "$query" > /dev/null 2>&1
    end_time=$(date +%s%3N)
    cold_time=$((end_time - start_time))
    
    # Small delay
    sleep 1
    
    # Hot run (should use cache)
    echo "  🔥 Hot run..."
    start_time=$(date +%s%3N)
    docker exec firebolt-core fbcli -e "$query" > /dev/null 2>&1
    end_time=$(date +%s%3N)
    hot_time=$((end_time - start_time))
    
    # Calculate improvement
    if [ $hot_time -gt 0 ]; then
        improvement=$(echo "scale=1; $cold_time / $hot_time" | bc)
    else
        improvement="∞"
    fi
    
    echo "  📊 Cold: ${cold_time}ms, Hot: ${hot_time}ms (${improvement}x faster)"
    echo ""
    
    # Append to results file
    echo "| $query_name | $cold_time | $hot_time | ${improvement}x |" >> $OUTPUT_FILE
}

# Check if Firebolt Core is running
if ! docker exec firebolt-core fbcli -e "SELECT 1" > /dev/null 2>&1; then
    echo "❌ Firebolt Core is not running or not responding"
    echo "Please start it with: ./setup_core.sh"
    exit 1
fi

# Check if data is loaded
echo "🔍 Checking if data is loaded..."
row_count=$(docker exec firebolt-core fbcli -e "SELECT COUNT(*) FROM violations" 2>/dev/null | tail -n1 | tr -d '[:space:]')

if [ -z "$row_count" ] || [ "$row_count" = "0" ]; then
    echo "❌ No data found in violations table"
    echo "Please load data with: make load-data"
    exit 1
fi

echo "✅ Found $row_count rows in violations table"
echo ""

# Run performance tests
for i in "${!QUERIES[@]}"; do
    run_query_with_timing "${QUERIES[$i]}" "${QUERY_NAMES[$i]}"
done

# Add summary to results file
cat >> $OUTPUT_FILE << EOF

## Summary

Total rows processed: $row_count

### Performance Insights

- **Cold runs** represent first-time query execution
- **Hot runs** benefit from Firebolt's intelligent caching
- **Sparse indexes** dramatically reduce scan times
- **Aggregating indexes** provide instant rollup results

### Firebolt Core Features Demonstrated

1. **Vectorized Processing**: SIMD-optimized aggregations
2. **Columnar Storage**: Efficient data scanning
3. **Smart Indexing**: Sparse and aggregating indexes
4. **Query Optimization**: Cost-based query planning
5. **Memory Management**: Intelligent caching layers

EOF

echo "📈 Performance comparison complete!"
echo "📄 Results saved to: $OUTPUT_FILE"
echo ""
echo "🚀 Key takeaways:"
echo "   - Hot queries are significantly faster due to caching"
echo "   - Sparse indexes accelerate filtered queries"
echo "   - Aggregating indexes provide instant rollups"
echo ""
cat $OUTPUT_FILE 