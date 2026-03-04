<?php

namespace App\Http\Controllers;

use App\Models\Transaction;

class TransactionController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        //
        // Rows per page.
        $row_per_page = 10;

        // Get the transactions of this page, ordered by date placed descending,
        // and then by unique id to make pagination stable.
        $TransactionPaginate = Transaction::orderBy('created_at', 'desc')
            ->orderBy('id', 'desc')
            ->with('Product')
            ->with('User')
            ->with('PayType')
            ->paginate($row_per_page);

        // Set the title and data for view.
        $binding = [
            'title' => __('shop.transaction.Transactions-list'),
            'TransactionPaginate'=> $TransactionPaginate,
        ];

        /**
         * If $hasDiscount is true, it will use the view 'Transactions.listTransactionSave.blade.php' with 'discount' column in the its table to list the transactions.
         * If $hasDiscount is false, it will use the view 'Transactions.listTransaction.blade.php' without 'discount' column in the its table to list the transactions.
         */
        $hasDiscount = false;
        if($hasDiscount) {
            // Sent the Transactions data to view with the column 'discount'.
            return view('transactions.listTransactionSave', $binding);
        }
        else {
            // Sent the Transactions data to view without the column 'discount'.
            return view('transactions.listTransaction', $binding);
        }
    }

    /**
     * Display the specified resource.
     */
    public function show($transaction_id)
    {
        $transaction = Transaction::findOrFail($transaction_id);
        //
        $binding = [
            'title' => __('shop.transaction.Order-details'),
            'Transaction'=> $transaction,
        ];
        return view('transactions.showTransaction', $binding);
    }

    /**
     * Display the specified resource.
     */
    public function listUserTransations($user_id)
    {
        // Rows per page.
        $row_per_page = 10;

        // Get the transactions of this page, ordered by date placed and unique id.
        $TransactionPaginate = Transaction::where('user_id', $user_id)
            ->orderBy('created_at', 'desc')
            ->orderBy('id', 'desc')
            ->with('Product')
            ->with('User')
            ->with('PayType')
            ->paginate($row_per_page);

        // Set the title and data for view.
        $binding = [
            'title' => __('shop.transaction.Your-histroy-orders'),
            'TransactionPaginate'=> $TransactionPaginate,
        ];

        // Sent the Transactions data to view.
        return view('transactions.listUserTransaction', $binding);
    }
}
