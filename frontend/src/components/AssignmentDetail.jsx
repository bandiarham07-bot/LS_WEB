import { useState } from 'react'
import ContentBlockRenderer from './blocks/ContentBlockRenderer'
import { useSubmitAssignment } from '../hooks/useSubmitAssignment'
import { useToast } from './Toast'

function formatDateTime(value) {
  if (!value) return 'Not set'
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

function getErrorMessage(error) {
  const data = error?.response?.data
  if (!data) return 'Submission failed. Please try again.'
  return data.error || data.roll_number || data.github_repo_url || 'Submission failed. Please try again.'
}

function formatGrade(submission) {
  if (!submission?.has_grade) return 'Not graded yet'
  if (submission.grade_awarded == null) return 'Feedback added'
  if (submission.grade_total == null) return submission.grade_awarded
  return `${submission.grade_awarded} / ${submission.grade_total}`
}

function InfoPanel({ title, children }) {
  return (
    <section className="bg-white border border-gray-100 rounded-2xl p-6">
      <h2 className="text-sm font-semibold text-gray-900 mb-3">{title}</h2>
      {children}
    </section>
  )
}

export default function AssignmentDetail({ page }) {
  const assignment = page.assignment
  const isUrlSubmission = assignment.submission_type === 'url'
  const [repoUrl, setRepoUrl] = useState(
    assignment?.submission?.github_repo_url || ''
  )
  const [rollNumber, setRollNumber] = useState(
    assignment?.submission?.roll_number || ''
  )
  const { showToast } = useToast()
  const submitAssignment = useSubmitAssignment(page.id, assignment.id)

  function handleSubmit(event) {
    event.preventDefault()
    submitAssignment.mutate({ githubRepoUrl: repoUrl, rollNumber }, {
      onSuccess: (submission) => {
        showToast(`Submitted ${submission.github_repo_name}`)
      },
    })
  }

  const submission = assignment.submission
  const isClosed = !assignment.is_open
  const errorMessage = submitAssignment.isError
    ? getErrorMessage(submitAssignment.error)
    : ''

  return (
    <div className="flex flex-col gap-4 mb-8">
      <InfoPanel title="Assignment details">
        {assignment.details && (
          <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap mb-4">
            {assignment.details}
          </div>
        )}

        <div className="flex flex-col gap-4">
          {page.blocks.map(block => (
            <ContentBlockRenderer key={block.id} block={block} />
          ))}
        </div>

        {!assignment.details && page.blocks.length === 0 && (
          <p className="text-sm text-gray-400">No assignment details added yet.</p>
        )}
      </InfoPanel>

      <InfoPanel title="Assignment due date">
        <div className="flex flex-wrap items-center gap-3">
          <p className="text-sm font-medium text-gray-900">
            {formatDateTime(assignment.due_date)}
          </p>
          <span
            className={
              'px-2.5 py-1 rounded-full text-xs font-medium ' +
              (assignment.is_open
                ? 'bg-emerald-50 text-emerald-700'
                : 'bg-gray-100 text-gray-500')
            }
          >
            {assignment.is_open ? 'Open for submissions' : 'Submissions closed'}
          </span>
        </div>
        {assignment.opens_at && (
          <p className="text-xs text-gray-400 mt-2">
            Opens {formatDateTime(assignment.opens_at)}
          </p>
        )}
      </InfoPanel>

      <InfoPanel title="Assignment deliverables">
        <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
          {assignment.deliverables}
        </div>
      </InfoPanel>

      <InfoPanel title="Assignment weightage">
        <p className="text-sm text-gray-700">
          {assignment.weightage || 'Not specified'}
        </p>
      </InfoPanel>

      <InfoPanel title="Assignment grade">
        {!submission ? (
          <p className="text-sm text-gray-500">
            {isUrlSubmission
              ? 'Submit your website link to see evaluation updates here.'
              : 'Submit your repository to see evaluation updates here.'}
          </p>
        ) : (
          <div className="flex flex-col gap-3">
            <div>
              <p className="text-xs font-semibold text-gray-500 mb-1">Awarded grade</p>
              <p
                className={
                  'text-lg font-semibold ' +
                  (submission.has_grade ? 'text-gray-900' : 'text-gray-400')
                }
              >
                {formatGrade(submission)}
              </p>
              {submission.graded_at && (
                <p className="text-xs text-gray-400 mt-1">
                  Graded {formatDateTime(submission.graded_at)}
                </p>
              )}
            </div>

            <div>
              <p className="text-xs font-semibold text-gray-500 mb-1">Evaluator note</p>
              {submission.evaluator_note ? (
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {submission.evaluator_note}
                </p>
              ) : (
                <p className="text-sm text-gray-500">
                  No evaluator note has been added yet.
                </p>
              )}
            </div>
          </div>
        )}
      </InfoPanel>

      <InfoPanel title="Assignment submission form">
        {submission && (
          <div className="mb-4 rounded-xl border border-[#d9e4f2] bg-[#f7f9fc] p-4">
            <p className="text-xs font-semibold text-gray-500 mb-1">Current submission</p>
            <a
              href={submission.github_repo_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-[#4a6fa5] hover:text-[#345280] break-all"
            >
              {submission.github_repo_name}
            </a>
            <p className="text-xs text-gray-400 mt-2">
              Submitted {formatDateTime(submission.submitted_at)}
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Roll number: {submission.roll_number}
            </p>
          </div>
        )}

        {isClosed ? (
          <p className="text-sm text-gray-500">
            The due date has passed, so new submissions are closed.
          </p>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <label className="text-xs font-semibold text-gray-500" htmlFor="roll_number">
              Roll number
            </label>
            <input
              id="roll_number"
              type="text"
              value={rollNumber}
              onChange={(event) => setRollNumber(event.target.value)}
              placeholder="Enter your roll number"
              className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition-colors focus:border-[#4a6fa5] focus:ring-2 focus:ring-[#d9e4f2]"
              required
            />
            <label className="text-xs font-semibold text-gray-500" htmlFor="github_repo_url">
              {isUrlSubmission ? 'Website Link' : 'GitHub repository link'}
            </label>
            <input
              id="github_repo_url"
              type="url"
              value={repoUrl}
              onChange={(event) => setRepoUrl(event.target.value)}
              placeholder={isUrlSubmission ? 'https://your-project.com': 'https://github.com/username/repository'}
              className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition-colors focus:border-[#4a6fa5] focus:ring-2 focus:ring-[#d9e4f2]"
              required
            />
            {errorMessage && (
              <p className="text-sm text-red-600">{errorMessage}</p>
            )}
            <button
              type="submit"
              disabled={submitAssignment.isPending}
              className="self-start px-5 py-2.5 bg-[#4a6fa5] text-white text-sm font-medium rounded-xl hover:bg-[#3d5e8e] disabled:cursor-not-allowed disabled:opacity-60 transition-colors"
            >
              {submitAssignment.isPending
                ? 'Submitting...'
                : submission
                  ? isUrlSubmission ? 'Update link' : 'Update submission'
                  : isUrlSubmission ? 'Submit link' : 'Submit repository'}
            </button>
          </form>
        )}
      </InfoPanel>
    </div>
  )
}
