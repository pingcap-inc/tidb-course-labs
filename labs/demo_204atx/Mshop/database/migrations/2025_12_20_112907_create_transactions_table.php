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
        Schema::create('transactions', function (Blueprint $table) {
            // Transaction ID.
            $table->id('id');
            // User ID.
            $table->unsignedBigInteger('user_id');
            // Merchandise ID.
            $table->unsignedBigInteger('product_id');
            // Price.
            $table->decimal('price',10,2);
            // Count.
            $table->integer('buy_count');
            // Total price.
            $table->decimal('total_price', 18, 2);
            // Timestamp.
            $table->timestamps();
            // Pay type.
            $table->string('pay_type', 16)->default('1');

            // Index
            $table->index(['user_id'], 'user_transaction_idx');
            $table->index(['product_id'], 'product_transaction_idx');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('transactions');
    }
};
