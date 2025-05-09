import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class MultithreadingDemo {

    private static final DateTimeFormatter TIME_FORMATTER = DateTimeFormatter.ofPattern("HH:mm:ss");
    private static final int NUMBER_OF_THREADS = 4;
    private static final int MIN_COMPLETION_TIME = 30;
    private static final int MAX_COMPLETION_TIME = 40;
    private static final int TIMEOUT_SECONDS = 60; // 1 minute timeout

    public static void main(String[] args) {
        System.out.println("Starting Main Method");

        // Test Case 1: All threads execute successfully
        System.out.println("\n--- Test Case 1: All threads execute successfully ---");
        boolean result1 = executeMultithreadedTask(false, false);
        System.out.println("Main method received result: " + (result1 ? "Success" : "Failure"));

        // Test Case 2: One thread fails with exception
        System.out.println("\n--- Test Case 2: One thread fails with exception ---");
        boolean result2 = executeMultithreadedTask(true, false);
        System.out.println("Main method received result: " + (result2 ? "Success" : "Failure"));
        
        // Test Case 3: One thread times out (doesn't return event within timeout)
        System.out.println("\n--- Test Case 3: One thread times out ---");
        boolean result3 = executeMultithreadedTask(false, true);
        System.out.println("Main method received result: " + (result3 ? "Success" : "Failure"));

        System.out.println("\nMain Method completed");
    }

    /**
     * Child method that spawns and manages multiple threads
     * 
     * @param simulateFailure Flag to simulate a failure in one thread
     * @param simulateTimeout Flag to simulate a timeout in one thread
     * @return true if all threads completed successfully, false if any thread failed
     */
    private static boolean executeMultithreadedTask(boolean simulateFailure, boolean simulateTimeout) {
        System.out.println("Starting child method");
        
        // Create thread pool with fixed number of threads
        ExecutorService executorService = Executors.newFixedThreadPool(NUMBER_OF_THREADS);
        
        // Create CountDownLatch to ensure all threads complete before returning
        CountDownLatch completionLatch = new CountDownLatch(NUMBER_OF_THREADS);
        
        // Create list to track futures for each task
        List<Future<WorkerEvent>> futures = new ArrayList<>();
        
        // AtomicBoolean to track if all threads succeeded
        AtomicBoolean allSuccessful = new AtomicBoolean(true);
        
        try {
            // Submit tasks to the executor
            for (int i = 0; i < NUMBER_OF_THREADS; i++) {
                int threadId = i + 1;
                boolean shouldFail = simulateFailure && threadId == 3; // Make thread #3 fail
                boolean shouldTimeout = simulateTimeout && threadId == 2; // Make thread #2 timeout
                
                // Create and submit a callable task
                Future<WorkerEvent> future = executorService.submit(() -> {
                    try {
                        return workerMethod(threadId, shouldFail, shouldTimeout);
                    } finally {
                        // Ensure latch is counted down even if exception occurs
                        completionLatch.countDown();
                        System.out.println("Thread " + threadId + " counted down latch: " + 
                                           completionLatch.getCount() + " remaining");
                    }
                });
                futures.add(future);
            }
            
            System.out.println("Child method waiting for all threads to complete...");
            
            // Process all futures with timeout
            for (int i = 0; i < futures.size(); i++) {
                Future<WorkerEvent> future = futures.get(i);
                int threadId = i + 1;
                
                try {
                    // Wait for result with timeout
                    WorkerEvent event = future.get(TIMEOUT_SECONDS, TimeUnit.SECONDS);
                    System.out.println("Thread " + threadId + " returned event: " + event);
                    
                    if (!event.isSuccess()) {
                        allSuccessful.set(false);
                    }
                } catch (TimeoutException e) {
                    System.out.println("Thread " + threadId + " timed out after " + TIMEOUT_SECONDS + " seconds");
                    allSuccessful.set(false);
                    // Cancel with interruption and ensure it's properly shut down
                    boolean wasCancelled = future.cancel(true);
                    System.out.println("Thread " + threadId + " cancellation result: " + 
                                      (wasCancelled ? "Successfully cancelled" : "Could not cancel"));
                    // Note: The finally block in the task will still count down the latch
                } catch (ExecutionException e) {
                    System.out.println("Thread " + threadId + " execution failed: " + e.getCause().getMessage());
                    allSuccessful.set(false);
                }
            }
            
            // Wait for all threads to count down the latch, with a timeout
            System.out.println("Waiting for completion latch (all threads to finish)...");
            boolean allThreadsCompleted = completionLatch.await(TIMEOUT_SECONDS * 2, TimeUnit.SECONDS);
            
            if (!allThreadsCompleted) {
                System.out.println("WARNING: Not all threads completed within the extended timeout period");
                allSuccessful.set(false);
            } else {
                System.out.println("All threads have completed their execution (latch reached zero)");
            }
            
        } catch (InterruptedException e) {
            System.out.println("Child method was interrupted: " + e.getMessage());
            Thread.currentThread().interrupt(); // Restore the interrupted status
            allSuccessful.set(false);
        } finally {
            // Initiate an orderly shutdown in which previously submitted tasks are executed,
            // but no new tasks will be accepted
            executorService.shutdown();
            
            try {
                // Wait for tasks to finish, with a timeout
                if (!executorService.awaitTermination(1, TimeUnit.MINUTES)) {
                    // Force shutdown if tasks don't complete within the timeout
                    executorService.shutdownNow();
                    System.out.println("ExecutorService was forcibly shutdown");
                }
            } catch (InterruptedException e) {
                System.out.println("Shutdown was interrupted: " + e.getMessage());
                executorService.shutdownNow();
                Thread.currentThread().interrupt(); // Restore the interrupted status
                allSuccessful.set(false);
            }
        }
        
        System.out.println("Child method returning " + allSuccessful.get());
        return allSuccessful.get();
    }

    /**
     * Worker method that simulates a long-running task and returns an event
     * 
     * @param threadId ID of the thread
     * @param shouldFail Flag to simulate failure
     * @param shouldTimeout Flag to simulate timeout (thread never returns an event)
     * @return WorkerEvent containing the result of the operation
     * @throws InterruptedException if the thread is interrupted
     */
    private static WorkerEvent workerMethod(int threadId, boolean shouldFail, boolean shouldTimeout) 
            throws InterruptedException {
        String threadName = "Thread " + threadId;
        System.out.println(threadName + " started at " + formatCurrentTime());
        
        try {
            // Generate random completion time between MIN_COMPLETION_TIME and MAX_COMPLETION_TIME seconds
            Random random = new Random();
            int completionTime = random.nextInt(MAX_COMPLETION_TIME - MIN_COMPLETION_TIME + 1) + MIN_COMPLETION_TIME;
            System.out.println(threadName + " will complete in " + completionTime + " seconds");
            
            // If simulating timeout, set a very long completion time
            if (shouldTimeout) {
                System.out.println(threadName + " is set to simulate timeout (will never complete)");
                // We'll sleep for much longer than the timeout period
                completionTime = TIMEOUT_SECONDS * 2;
            }
            
            // Simulate work progress
            for (int i = 1; i <= completionTime; i++) {
                // If this thread should fail, throw an exception after 5 seconds
                if (shouldFail && i == 5) {
                    throw new RuntimeException("Simulated failure in " + threadName);
                }
                
                // Check if thread has been interrupted BEFORE sleeping
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println(threadName + " was interrupted at " + i + " seconds");
                    throw new InterruptedException("Thread was interrupted during execution");
                }
                
                System.out.println(threadName + " working... (" + i + " seconds)");
                
                // Sleep for shorter intervals to be more responsive to interrupts
                for (int j = 0; j < 10; j++) {
                    Thread.sleep(100); // Sleep for 100ms (10 times = 1 second total)
                    if (Thread.currentThread().isInterrupted()) {
                        System.out.println(threadName + " was interrupted during sleep at " + i + " seconds");
                        throw new InterruptedException("Thread was interrupted during execution");
                    }
                }
            }
            
            // Create successful event
            System.out.println(threadName + " completed successfully at " + formatCurrentTime());
            return new WorkerEvent(threadId, true, "Task completed successfully", formatCurrentTime());
        } catch (RuntimeException e) {
            System.out.println(threadName + " failed with exception: " + e.getMessage() + " at " + formatCurrentTime());
            return new WorkerEvent(threadId, false, e.getMessage(), formatCurrentTime());
        }
    }
    
    /**
     * Format current time
     * 
     * @return formatted time string
     */
    private static String formatCurrentTime() {
        return LocalTime.now().format(TIME_FORMATTER);
    }
    
    /**
     * Event class to represent the result of a worker thread
     */
    static class WorkerEvent {
        private final int threadId;
        private final boolean success;
        private final String message;
        private final String timestamp;
        
        public WorkerEvent(int threadId, boolean success, String message, String timestamp) {
            this.threadId = threadId;
            this.success = success;
            this.message = message;
            this.timestamp = timestamp;
        }
        
        public int getThreadId() {
            return threadId;
        }
        
        public boolean isSuccess() {
            return success;
        }
        
        public String getMessage() {
            return message;
        }
        
        public String getTimestamp() {
            return timestamp;
        }
        
        @Override
        public String toString() {
            return "WorkerEvent{" +
                    "threadId=" + threadId +
                    ", success=" + success +
                    ", message='" + message + '\'' +
                    ", timestamp='" + timestamp + '\'' +
                    '}';
        }
    }
}