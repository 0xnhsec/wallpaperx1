#!/bin/bash

# Script untuk mengurutkan dan mengganti nama file gambar
# Ekstensi yang didukung: .jpg, .jpeg, .png, .webp, .svg

# Warna untuk output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Direktori target (default: direktori saat ini)
TARGET_DIR="${1:-.}"

# Pindah ke direktori target
cd "$TARGET_DIR" || exit 1

echo -e "${CYAN}🔍 Mencari file gambar di: $(pwd)${NC}"

# Array ekstensi yang didukung
declare -a EXTENSIONS=("jpg" "jpeg" "png" "webp" "svg")

# Array untuk menyimpan semua file gambar yang ditemukan
declare -a ALL_IMAGES=()

# Cari semua file gambar (case-insensitive)
for ext in "${EXTENSIONS[@]}"; do
    while IFS= read -r -d '' file; do
        ALL_IMAGES+=("$file")
    done < <(find . -maxdepth 1 -type f -iname "*.${ext}" -print0 2>/dev/null)
done

# Hitung jumlah file
total_files=${#ALL_IMAGES[@]}

if [ "$total_files" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Tidak ada file gambar ditemukan (.jpg, .jpeg, .png, .webp, .svg)${NC}"
    exit 0
fi

echo -e "${GREEN}📁 Ditemukan $total_files file gambar${NC}"
echo ""

# Tanya user apakah ingin mengurutkan ulang dari 1 atau melanjutkan
read -p "Urutkan ulang dari 1? (y/n, default=y): " -n 1 -r
echo ""
RENUMBER_FROM_ONE=${REPLY:-y}

if [[ $RENUMBER_FROM_ONE =~ ^[Yy]$ ]]; then
    start_number=1
    echo -e "${CYAN}🚀 Mengurutkan ulang dari nomor: 1${NC}"
else
    # Cari nomor terbesar yang sudah ada
    max_number=0
    for file in "${ALL_IMAGES[@]}"; do
        filename=$(basename "$file")
        name="${filename%.*}"
        
        if [[ "$name" =~ ^[0-9]+$ ]]; then
            if [ "$name" -gt "$max_number" ]; then
                max_number="$name"
            fi
        fi
    done
    
    start_number=$((max_number + 1))
    echo -e "${CYAN}🔢 Nomor terakhir yang ada: $max_number${NC}"
    echo -e "${CYAN}🚀 Memulai penomoran dari: $start_number${NC}"
fi

echo ""

# Sort file berdasarkan waktu modifikasi (terlama dulu)
IFS=$'\n' sorted_files=($(for img in "${ALL_IMAGES[@]}"; do
    stat -c '%Y %n' "$img" 2>/dev/null || stat -f '%m %N' "$img" 2>/dev/null
done | sort -n | cut -d' ' -f2-))

# Jika sorting berdasarkan waktu gagal, gunakan sorting berdasarkan nama
if [ ${#sorted_files[@]} -eq 0 ]; then
    IFS=$'\n' sorted_files=($(printf '%s\n' "${ALL_IMAGES[@]}" | sort -V))
fi

# Gunakan direktori temporary untuk menghindari konflik nama
TEMP_DIR=$(mktemp -d)
echo -e "${CYAN}📦 Menggunakan direktori temporary: $TEMP_DIR${NC}"
echo ""

# Counter
current=0
renamed=0
next_number=$start_number

# Fase 1: Pindahkan ke temporary dengan nama baru
for file in "${sorted_files[@]}"; do
    ((current++))
    
    filename=$(basename "$file")
    extension="${filename##*.}"
    extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
    
    # Format nomor tanpa leading zeros
    new_name="${next_number}.${extension}"
    
    # Copy ke temporary directory
    cp "$file" "$TEMP_DIR/$new_name"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ [$current/$total_files] $filename → $new_name${NC}"
        ((renamed++))
        ((next_number++))
    else
        echo -e "${RED}  ❌ [$current/$total_files] Gagal copy: $filename${NC}"
    fi
done

echo ""
echo -e "${YELLOW}🔄 Memindahkan file kembali dari temporary...${NC}"

# Fase 2: Hapus file lama dan pindahkan file baru
for file in "${ALL_IMAGES[@]}"; do
    rm -f "$file"
done

# Pindahkan dari temporary kembali ke direktori asli
mv "$TEMP_DIR"/* . 2>/dev/null

# Hapus temporary directory
rmdir "$TEMP_DIR"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Selesai!${NC}"
echo -e "${GREEN}   Total file: $total_files${NC}"
echo -e "${GREEN}   Di-rename:  $renamed${NC}"
echo -e "${GREEN}   Range:      $start_number - $((next_number - 1))${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
