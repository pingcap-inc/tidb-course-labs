<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('products', function (Blueprint $table) {
            //ID
            $table->id('id');
            // Used to indicate the status of products; only products that have been listed can be seen by consumers.
            //  - C（Create）: Under Construction
            //  - S（Sell）: Available for Sale
            $table->string('status', 1)->default('C');
            // Product Name
            $table->string('name', 80)->nullable()->index('idx_name_product');
            // Product Description
            $table->text('introduction');
            // Product Photo
            $table->string('photo', 50)->nullable();
            // Price
             $table->decimal('price',10,2)->default(0.00);
            // Quantity Remaining
            $table->integer('remain_count')->default(0);
            // Timestamp
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
