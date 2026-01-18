REPO_URL="https://github.com/jaydeep1305/test-adc-zip-data/archive/refs/heads/main.zip"

# Extract repo name and branch from URL dynamically
REPO_PATH=$(echo "$REPO_URL" | sed 's|https://github.com/||' | sed 's|/archive/refs/heads/.*||')
REPO_NAME=$(basename "$REPO_PATH")
BRANCH=$(echo "$REPO_URL" | sed 's|.*/archive/refs/heads/||' | sed 's|\.zip||')
EXTRACTED_DIR="${REPO_NAME}-${BRANCH}"

echo "Extracting $REPO_NAME ($BRANCH branch) to test..."

mkdir -p "test" && cd "test" && \
wget "$REPO_URL" -O temp.zip && \
unzip temp.zip && \
if [ -d "$EXTRACTED_DIR" ]; then
    mv "$EXTRACTED_DIR"/* . 2>/dev/null || true
    mv "$EXTRACTED_DIR"/.* . 2>/dev/null || true
    rm -rf "$EXTRACTED_DIR"
fi && \
rm -f temp.zip && \
echo "Extracted to test"