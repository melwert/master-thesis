package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type GeneralStatistic struct {
	Id                    primitive.ObjectID `bson:"_id" json:"id"`
	CommitCount           int                `bson:"commit_count" json:"commitCount"`
	FileCount             int                `bson:"file_count" json:"fileCount"`
	DeveloperCount        int                `bson:"developer_count" json:"developerCount"`
	RepositoryLink        string             `bson:"repository_link" json:"repositoryLink"`
	BitbucketCommentCount int                `bson:"bitbucket_comment_count" json:"bitbucketCommentCount"`
	BitbucketPrCount      int                `bson:"bitbucket_pr_count" json:"bitbucketPrCount"`
	BranchCount           int                `bson:"branch_count" json:"branchCount"`
	JiraIssueCount        int                `bson:"jira_issue_count" json:"jiraIssueCount"`
	FileEndings           []string           `bson:"fileendings" json:"fileEndings"`
	LastScanDate          time.Time          `bson:"last_scan_date" json:"lastScanDate"`
	ProjectId             primitive.ObjectID `bson:"project_id" json:"projectId"`
}
