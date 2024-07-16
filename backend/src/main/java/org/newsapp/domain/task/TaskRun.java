package org.newsapp.domain.task;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.newsapp.dto.task.UpdateTaskRunDTO;

import java.time.ZonedDateTime;

@RequiredArgsConstructor
@Getter
@Entity
public class TaskRun {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TaskRunStatus status;
    private ZonedDateTime createdAt;
    private ZonedDateTime finishedAt;
    private Long success;
    private Long failed;

    @PrePersist
    public void prePersist() {
        this.createdAt = ZonedDateTime.now();
    }

    public TaskRun(Task task) {
        this.task = task;
        this.status = TaskRunStatus.CREATED;
    }

    public void updateStatus(TaskRunStatus status) {
        this.status = status;
    }

    public void update(UpdateTaskRunDTO dto) {
        this.status = dto.getStatus();
        if (status.equals(TaskRunStatus.DONE)) {
            this.finishedAt = ZonedDateTime.now();
            this.success = dto.getSuccess();
            this.failed = dto.getFailed();
        }
    }
}

