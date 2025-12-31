<?php

namespace App\Http\Controllers;

use App\Models\Transaction;
use APP\Models\User;
use Illuminate\Http\Request;

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

        // Get the transactions of this page.
        $TransactionPaginate = Transaction::OrderBy('created_at', 'desc')
        ->OrderBy('user_id','desc')
        ->with('Product')
        ->with('User')
        ->paginate($row_per_page);

        // Set the title and data for view.
        $binding = [
            'title' => 'Transactions list',
            'TransactionPaginate'=> $TransactionPaginate,
        ];

        // Sent the Transactions data to view.
        return view('Transactions.listTransaction', $binding);

    }

    /**
     * Display a listing of the resource.
     */
    public function listUserTransactions()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show($transaction_id)
    {
        $transaction = Transaction::findOrFail($transaction_id);
        //
        $binding = [
            'title' => 'Order Details',
            'Transaction'=> $transaction,
        ];
        return view('transactions.ShowTransaction', $binding);
    }

    /**
     * Display the specified resource.
     */
    public function listUserTransations($user_id)
    {
        // Rows per page.
        $row_per_page = 10;

        // Get the transactions of this page.
        $TransactionPaginate = Transaction::where('user_id', $user_id)
            ->OrderBy('created_at', 'desc')
            ->with('Product')
            ->with('User')
            ->paginate($row_per_page);

        // Set the title and data for view.
        $binding = [
            'title' => "Your histroy orders:" ,
            'TransactionPaginate'=> $TransactionPaginate,
        ];

        // Sent the Transactions data to view.
        return view('Transactions.listUserTransaction', $binding);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Transaction $transaction)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Transaction $transaction)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Transaction $transaction)
    {
        //
    }
}
